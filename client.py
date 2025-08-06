
from typing import Any
from uuid import uuid4
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)
from a2a.utils.constants import (
    AGENT_CARD_WELL_KNOWN_PATH,
    EXTENDED_AGENT_CARD_PATH,
)
from loguru import logger


async def chat_mode(agent_url: str = "http://localhost:9999"):
    logger.info(f"Starting chat mode for agent at {agent_url}")
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=agent_url
        )
        _public_card = await resolver.get_agent_card()
        final_agent_card_to_use = _public_card
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=final_agent_card_to_use
        )
        logger.info('A2AClient initialized for chat mode.')
        while True:
            user_input = input("You: ")
            if user_input.lower() in ("exit", "quit"):
                break
            send_message_payload: dict[str, Any] = {
                'message': {
                    'role': 'user',
                    'parts': [
                        {'kind': 'text', 'text': user_input}
                    ],
                    'messageId': uuid4().hex,
                },
            }
            streaming_request = SendStreamingMessageRequest(
                id=str(uuid4()), params=MessageSendParams(**send_message_payload)
            )
            stream_response = client.send_message_streaming(streaming_request)
            async for chunk in stream_response:
                print(chunk.model_dump(mode='json', exclude_none=True))


async def main(agent_url: str = "http://localhost:9999"):
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=agent_url,
        )
        final_agent_card_to_use: AgentCard | None = None
        try:
            logger.info(
                f'Attempting to fetch public agent card from: {agent_url}{AGENT_CARD_WELL_KNOWN_PATH}'
            )
            _public_card = (
                await resolver.get_agent_card()
            )
            logger.info('Successfully fetched public agent card:')
            logger.info(
                _public_card.model_dump_json(indent=2, exclude_none=True)
            )
            final_agent_card_to_use = _public_card
            logger.info(
                '\nUsing PUBLIC agent card for client initialization (default).'
            )
            if _public_card.supports_authenticated_extended_card:
                try:
                    logger.info(
                        f'\nPublic card supports authenticated extended card. Attempting to fetch from: {agent_url}{EXTENDED_AGENT_CARD_PATH}'
                    )
                    auth_headers_dict = {
                        'Authorization': 'Bearer dummy-token-for-extended-card'
                    }
                    _extended_card = await resolver.get_agent_card(
                        relative_card_path=EXTENDED_AGENT_CARD_PATH,
                        http_kwargs={'headers': auth_headers_dict},
                    )
                    logger.info(
                        'Successfully fetched authenticated extended agent card:'
                    )
                    logger.info(
                        _extended_card.model_dump_json(
                            indent=2, exclude_none=True
                        )
                    )
                    final_agent_card_to_use = (
                        _extended_card
                    )
                    logger.info(
                        '\nUsing AUTHENTICATED EXTENDED agent card for client initialization.'
                    )
                except Exception as e_extended:
                    logger.warning(
                        f'Failed to fetch extended agent card: {e_extended}. Will proceed with public card.',
                        exc_info=True,
                    )
            elif (
                _public_card
            ):
                logger.info(
                    '\nPublic card does not indicate support for an extended card. Using public card.'
                )
        except Exception as e:
            logger.error(
                f'Critical error fetching public agent card: {e}', exc_info=True
            )
            raise RuntimeError(
                'Failed to fetch the public agent card. Cannot continue.'
            ) from e
        client = A2AClient(
            httpx_client=httpx_client, 
            agent_card=final_agent_card_to_use
        )
        logger.info('A2AClient initialized.')
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': 'how much is 10 USD in INR?'}
                ],
                'messageId': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )
        response = await client.send_message(request)
        print(response.model_dump(mode='json', exclude_none=True))
        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )
        stream_response = client.send_message_streaming(streaming_request)
        async for chunk in stream_response:
            print(chunk.model_dump(mode='json', exclude_none=True))
            can_continue = input("Continue receiving messages? (y/n): ")
            if can_continue.lower() != 'y':
                break
        print("-" * 20)
        print("End of streaming response.")


if __name__ == '__main__':
    import asyncio
    import argparse
    parser = argparse.ArgumentParser(description="A2A Test Client")
    parser.add_argument("--agent", type=str, default="http://localhost:9999", help="URL of the A2A agent")
    parser.add_argument("--chat", action="store_true", help="Start in chat mode")
    args = parser.parse_args()
    if args.chat:
        asyncio.run(chat_mode(agent_url=args.agent))
    else:
        asyncio.run(main(agent_url=args.agent, chat_mode=args.chat))
