# # Copyright 2025 The OpenChoreo Authors
# # SPDX-License-Identifier: Apache-2.0

# import json
# import logging
# import time
# from collections.abc import Awaitable, Callable
# from typing import Any

# from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
# from langchain.messages import ToolMessage
# from langchain.tools.tool_node import ToolCallRequest
# from langchain_core.messages import AIMessage, HumanMessage
# from langgraph.types import Command

# logger = logging.getLogger(__name__)


# class LoggingMiddleware(AgentMiddleware):
#     def __init__(self) -> None:
#         super().__init__()
#         self.model_call_count: int = 0
#         self.tool_call_count: int = 0
#         self.tool_calls: list[dict[str, Any]] = []

#     async def awrap_model_call(
#         self,
#         request: ModelRequest,
#         handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
#     ) -> ModelResponse:
#         # Find last AI message and get everything after it
#         last_ai_idx = -1
#         for i in range(len(request.messages) - 1, -1, -1):
#             if isinstance(request.messages[i], AIMessage):
#                 last_ai_idx = i
#                 break

#         new_messages = request.messages[last_ai_idx + 1 :]

#         for message in new_messages:
#             if isinstance(message, HumanMessage):
#                 logger.debug("Human message: %s", message.content)

#         self.model_call_count += 1
#         logger.debug("Starting model call #%d", self.model_call_count)

#         start_time = time.time()
#         result = await handler(request)
#         elapsed = time.time() - start_time

#         logger.info("Model call #%d completed in %.2fs", self.model_call_count, elapsed)

#         ai_message = result.result[0]

#         if isinstance(ai_message, AIMessage) and ai_message.tool_calls:
#             for tool_call in ai_message.tool_calls:
#                 logger.debug(
#                     "Tool call: %s with args: %s", tool_call.get("name"), tool_call.get("args")
#                 )

#         return result

#     async def awrap_tool_call(
#         self,
#         request: ToolCallRequest,
#         handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
#     ) -> ToolMessage | Command:
#         tool_name = request.tool_call.get("name")
#         tool_args = request.tool_call.get("args")
#         start_time = time.time()

#         result = await handler(request)

#         elapsed = time.time() - start_time
#         self.tool_call_count += 1

#         if isinstance(result, ToolMessage) and result.content:
#             if isinstance(result.content, str):
#                 content_len = len(result.content)
#             elif isinstance(result.content, list):
#                 content_len = sum(
#                     len(b.get("text", "")) for b in result.content if isinstance(b, dict)
#                 )
#             else:
#                 content_len = 0
#         else:
#             content_len = 0
#         logger.info(
#             "Tool '%s' (#%d) took %.2fs, result: %d chars",
#             tool_name,
#             self.tool_call_count,
#             elapsed,
#             content_len,
#         )
#         logger.debug("Tool '%s' args: %s", tool_name, tool_args)

#         self.tool_calls.append({"name": tool_name, "args": tool_args, "elapsed": round(elapsed, 2)})

#         return result

#     def tool_call_summary(self) -> str | None:
#         if not self.tool_calls:
#             return None
#         return json.dumps(self.tool_calls, default=str)


# Copyright 2025 The OpenChoreo Authors
# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 The OpenChoreo Authors
# SPDX-License-Identifier: Apache-2.0

import asyncio
import json
import logging
import time
from collections import Counter
from collections.abc import Awaitable, Callable
from typing import Any

import anyio
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command

logger = logging.getLogger(__name__)

MODEL_CALL_TIMEOUT = 90          # hard wall-clock cap per model call
MAX_CALLS_PER_TOOL = 4           # cap on repeated identical-purpose tool calls


class LoggingMiddleware(AgentMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.model_call_count: int = 0
        self.tool_call_count: int = 0
        self.tool_calls: list[dict[str, Any]] = []
        self.tool_call_counts: Counter[str] = Counter()

    async def awrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
    ) -> ModelResponse:
        last_ai_idx = -1
        for i in range(len(request.messages) - 1, -1, -1):
            if isinstance(request.messages[i], AIMessage):
                last_ai_idx = i
                break

        new_messages = request.messages[last_ai_idx + 1 :]

        for message in new_messages:
            if isinstance(message, HumanMessage):
                logger.debug("Human message: %s", message.content)

        self.model_call_count += 1
        logger.debug("Starting model call #%d", self.model_call_count)

        start_time = time.time()
        try:
            with anyio.fail_after(MODEL_CALL_TIMEOUT):
                result = await handler(request)
        except TimeoutError:
            elapsed = time.time() - start_time
            logger.error(
                "Model call #%d exceeded %ds wall-clock timeout (ran %.2fs)",
                self.model_call_count, MODEL_CALL_TIMEOUT, elapsed,
            )
            raise
        except asyncio.CancelledError:
            elapsed = time.time() - start_time
            logger.error(
                "Model call #%d got raw CancelledError at %.2fs instead of TimeoutError — "
                "cancellation is being caught/reraised upstream (check for asyncio.shield "
                "in LangSmith tracing or LangGraph's runner)",
                self.model_call_count, elapsed,
            )
            raise
        elapsed = time.time() - start_time

        logger.info("Model call #%d completed in %.2fs", self.model_call_count, elapsed)

        ai_message = result.result[0]

        if isinstance(ai_message, AIMessage) and ai_message.tool_calls:
            for tool_call in ai_message.tool_calls:
                logger.debug(
                    "Tool call: %s with args: %s", tool_call.get("name"), tool_call.get("args")
                )

        return result

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
    ) -> ToolMessage | Command:
        tool_name = request.tool_call.get("name")
        tool_args = request.tool_call.get("args")

        self.tool_call_counts[tool_name] += 1
        if self.tool_call_counts[tool_name] > MAX_CALLS_PER_TOOL:
            logger.warning(
                "Tool '%s' exceeded %d calls — short-circuiting",
                tool_name, MAX_CALLS_PER_TOOL,
            )
            return ToolMessage(
                content=(
                    f"Tool call limit reached for '{tool_name}'. "
                    "No further calls to this tool are permitted — "
                    "proceed with the analysis using information already gathered."
                ),
                tool_call_id=request.tool_call.get("id"),
                name=tool_name,
            )

        start_time = time.time()
        result = await handler(request)
        elapsed = time.time() - start_time
        self.tool_call_count += 1

        if isinstance(result, ToolMessage) and result.content:
            if isinstance(result.content, str):
                content_len = len(result.content)
            elif isinstance(result.content, list):
                content_len = sum(
                    len(b.get("text", "")) for b in result.content if isinstance(b, dict)
                )
            else:
                content_len = 0
        else:
            content_len = 0
        logger.info(
            "Tool '%s' (#%d) took %.2fs, result: %d chars",
            tool_name,
            self.tool_call_count,
            elapsed,
            content_len,
        )
        logger.debug("Tool '%s' args: %s", tool_name, tool_args)

        self.tool_calls.append({"name": tool_name, "args": tool_args, "elapsed": round(elapsed, 2)})

        return result

    def tool_call_summary(self) -> str | None:
        if not self.tool_calls:
            return None
        return json.dumps(self.tool_calls, default=str)