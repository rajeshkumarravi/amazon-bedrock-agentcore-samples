# Cloudwatch masking regular expression test data

```json
{
    "resource": {
        "attributes": {
            "deployment.environment.name": "bedrock-agentcore:default",
            "aws.local.service": "acr_cmk_demo.DEFAULT",
            "service.name": "acr_cmk_demo.DEFAULT",
            "cloud.region": "us-east-1",
            "aws.log.stream.names": "otel-rt-logs",
            "telemetry.sdk.name": "opentelemetry",
            "aws.service.type": "gen_ai_agent",
            "telemetry.sdk.language": "python",
            "cloud.provider": "aws",
            "cloud.resource_id": "arn:aws:bedrock-agentcore:us-east-1:467801433859:runtime/acr_cmk_demo-nerCnuBMNU/runtime-endpoint/DEFAULT:DEFAULT",
            "aws.log.group.names": "/aws/bedrock-agentcore/runtimes/acr_cmk_demo-nerCnuBMNU-DEFAULT",
            "telemetry.sdk.version": "1.33.1",
            "cloud.platform": "aws_bedrock_agentcore",
            "telemetry.auto.version": "0.12.2-aws"
        }
    },
    "scope": {
        "name": "opentelemetry.instrumentation.instrumentor"
    },
    "timeUnixNano": 1777999625236330240,
    "observedTimeUnixNano": 1777999625236422463,
    "severityNumber": 13,
    "severityText": "WARN",
    "body": "Attempting to instrument while already instrumented",
    "attributes": {
        "otelTraceSampled": true,
        "code.file.path": "/usr/local/lib/python3.13/site-packages/opentelemetry/instrumentation/instrumentor.py",
        "code.function.name": "instrument",
        "otelTraceID": "69fa1f0879d01d2e2401006021a9e3d9",
        "otelSpanID": "7cba7f714dc8b6f2",
        "code.line.number": 103,
        "otelServiceName": "acr_cmk_demo.DEFAULT"
    },
    "flags": 1,
    "traceId": "69fa1f0879d01d2e2401006021a9e3d9",
    "spanId": "7cba7f714dc8b6f2"
}
{
    "resource": {
        "attributes": {
            "deployment.environment.name": "bedrock-agentcore:default",
            "aws.local.service": "restaurant_assistant_demo.DEFAULT",
            "service.name": "restaurant_assistant_demo.DEFAULT",
            "cloud.region": "us-east-1",
            "aws.log.stream.names": "otel-rt-logs",
            "telemetry.sdk.name": "opentelemetry",
            "aws.service.type": "gen_ai_agent",
            "telemetry.sdk.language": "python",
            "cloud.provider": "aws",
            "cloud.resource_id": "arn:aws:bedrock-agentcore:us-east-1:467801433859:runtime/restaurant_assistant_demo-N1g4Vp8Xrb/runtime-endpoint/DEFAULT:DEFAULT",
            "aws.log.group.names": "/aws/bedrock-agentcore/runtimes/restaurant_assistant_demo-N1g4Vp8Xrb-DEFAULT",
            "telemetry.sdk.version": "1.33.1",
            "cloud.platform": "aws_bedrock_agentcore",
            "telemetry.auto.version": "0.12.2-aws"
        }
    },
    "scope": {
        "name": "strands.telemetry.tracer"
    },
    "timeUnixNano": 1776870387242306543,
    "observedTimeUnixNano": 1776870387243297763,
    "severityNumber": 9,
    "severityText": "",
    "body": {
        "output": {
            "messages": [
                {
                    "content": {
                        "message": "[{\"text\": \"Memories retrieved successfully: {\\\"memoryRecordSummaries\\\": [{\\\"memoryRecordId\\\": \\\"mem-41c57c53-b0ab-40a8-9fe0-b8c8b0d403c2\\\", \\\"content\\\": {\\\"text\\\": \\\"{\\\\\\\"context\\\\\\\":\\\\\\\"The user explicitly stated they really like tofu and fresh vegetables in their dishes.\\\\\\\",\\\\\\\"preference\\\\\\\":\\\\\\\"Enjoys tofu and fresh vegetables in dishes\\\\\\\",\\\\\\\"categories\\\\\\\":[\\\\\\\"food\\\\\\\",\\\\\\\"ingredients\\\\\\\"]}\\\"}, \\\"memoryStrategyId\\\": \\\"UserPreferences-nITJioH0eb\\\", \\\"namespaces\\\": [\\\"/users/default_actor/preferences\\\"], \\\"createdAt\\\": \\\"2025-11-26 16:28:27.135000+00:00\\\", \\\"score\\\": 0.40564013, \\\"metadata\\\": {\\\"x-amz-agentcore-memory-recordType\\\": {\\\"stringValue\\\": \\\"BASE\\\"}}}, {\\\"memoryRecordId\\\": \\\"mem-a27ebd30-7adc-47c8-bc64-628b40004b44\\\", \\\"content\\\": {\\\"text\\\": \\\"{\\\\\\\"context\\\\\\\":\\\\\\\"The user explicitly mentioned enjoying Italian cuisine and loving pasta dishes that are vegetarian-friendly.\\\\\\\",\\\\\\\"preference\\\\\\\":\\\\\\\"Enjoys Italian cuisine, especially pasta dishes that are vegetarian\\\\\\\",\\\\\\\"categories\\\\\\\":[\\\\\\\"food\\\\\\\",\\\\\\\"cuisine\\\\\\\"]}\\\"}, \\\"memoryStrategyId\\\": \\\"UserPreferences-nITJioH0eb\\\", \\\"namespaces\\\": [\\\"/users/default_actor/preferences\\\"], \\\"createdAt\\\": \\\"2025-11-26 16:28:27.135000+00:00\\\", \\\"score\\\": 0.39190513, \\\"metadata\\\": {\\\"x-amz-agentcore-memory-recordType\\\": {\\\"stringValue\\\": \\\"BASE\\\"}}}, {\\\"memoryRecordId\\\": \\\"mem-013ea74d-9b22-4c6e-971f-0777c4486e6a\\\", \\\"content\\\": {\\\"text\\\": \\\"{\\\\\\\"context\\\\\\\":\\\\\\\"The user explicitly mentioned looking for vegetarian dishes to try this weekend.\\\\\\\",\\\\\\\"preference\\\\\\\":\\\\\\\"Looking for vegetarian dishes\\\\\\\",\\\\\\\"categories\\\\\\\":[\\\\\\\"food\\\\\\\",\\\\\\\"diet\\\\\\\"]}\\\"}, \\\"memoryStrategyId\\\": \\\"UserPreferences-nITJioH0eb\\\", \\\"namespaces\\\": [\\\"/users/default_actor/preferences\\\"], \\\"createdAt\\\": \\\"2025-11-26 16:28:27.135000+00:00\\\", \\\"score\\\": 0.38444135, \\\"metadata\\\": {\\\"x-amz-agentcore-memory-recordType\\\": {\\\"stringValue\\\": \\\"BASE\\\"}}}]}\"}]",
                        "id": "tooluse_xOV9KoGAjpkuzBfPbfTQKz"
                    },
                    "role": "assistant"
                }
            ]
        },
        "input": {
            "messages": [
                {
                    "content": {
                        "content": "{\"action\": \"retrieve\", \"query\": \"food preferences cuisine dietary restrictions\", \"max_results\": 5}",
                        "role": "tool",
                        "id": "tooluse_xOV9KoGAjpkuzBfPbfTQKz"
                    },
                    "role": "tool"
                }
            ]
        }
    },
    "attributes": {
        "event.name": "strands.telemetry.tracer",
        "session.id": "6be9ce38-8726-4045-b006-0b06dd627ed4"
    },
    "flags": 1,
    "traceId": "69e8e3ee24e8eb755250b36d063d7d98",
    "spanId": "a9c374049aedc61c"
}
{
    "resource": {
        "attributes": {
            "deployment.environment.name": "bedrock-agentcore:default",
            "aws.local.service": "acr_cmk_demo.DEFAULT",
            "service.name": "acr_cmk_demo.DEFAULT",
            "cloud.region": "us-east-1",
            "aws.log.stream.names": "otel-rt-logs",
            "telemetry.sdk.name": "opentelemetry",
            "aws.service.type": "gen_ai_agent",
            "telemetry.sdk.language": "python",
            "cloud.provider": "aws",
            "cloud.resource_id": "arn:aws:bedrock-agentcore:us-east-1:467801433859:runtime/acr_cmk_demo-nerCnuBMNU/runtime-endpoint/DEFAULT:DEFAULT",
            "aws.log.group.names": "/aws/bedrock-agentcore/runtimes/acr_cmk_demo-nerCnuBMNU-DEFAULT",
            "telemetry.sdk.version": "1.33.1",
            "cloud.platform": "aws_bedrock_agentcore",
            "telemetry.auto.version": "0.12.2-aws"
        }
    },
    "scope": {
        "name": "opentelemetry.instrumentation.botocore.bedrock-runtime",
        "schemaUrl": "https://opentelemetry.io/schemas/1.30.0"
    },
    "timeUnixNano": 1777999625339605916,
    "observedTimeUnixNano": 1777999625339613319,
    "severityNumber": 9,
    "severityText": "",
    "body": {
        "content": [
            {
                "text": "suggest sushi restaurants in nyc"
            }
        ]
    },
    "attributes": {
        "event.name": "gen_ai.user.message",
        "gen_ai.system": "aws.bedrock"
    },
    "flags": 1,
    "traceId": "69fa1f0879d01d2e2401006021a9e3d9",
    "spanId": "9e18e6dcbeace41d"
}
{
    "resource": {
        "attributes": {
            "deployment.environment.name": "bedrock-agentcore:default",
            "aws.local.service": "langgraph_rt_obsy_demo.DEFAULT",
            "service.name": "langgraph_rt_obsy_demo.DEFAULT",
            "cloud.region": "us-east-1",
            "aws.log.stream.names": "otel-rt-logs",
            "telemetry.sdk.name": "opentelemetry",
            "aws.service.type": "gen_ai_agent",
            "telemetry.sdk.language": "python",
            "cloud.provider": "aws",
            "cloud.resource_id": "arn:aws:bedrock-agentcore:us-east-1:467801433859:runtime/langgraph_rt_obsy_demo-W2asBi97E7/runtime-endpoint/DEFAULT:DEFAULT",
            "aws.log.group.names": "/aws/bedrock-agentcore/runtimes/langgraph_rt_obsy_demo-W2asBi97E7-DEFAULT",
            "telemetry.sdk.version": "1.40.0",
            "cloud.platform": "aws_bedrock_agentcore",
            "telemetry.auto.version": "0.17.0-aws"
        }
    },
    "scope": {
        "name": "opentelemetry.instrumentation.langchain"
    },
    "timeUnixNano": 1776808993612878753,
    "observedTimeUnixNano": 1776808998105207401,
    "severityNumber": 9,
    "severityText": "",
    "body": {
        "output": {
            "messages": [
                {
                    "content": "{\"output\": {\"lc\": 1, \"type\": \"constructor\", \"id\": [\"langchain\", \"schema\", \"messages\", \"ToolMessage\"], \"kwargs\": {\"content\": \"1. Best Vegetarian and Vegan Restaurants in Austin to Try... - Thrillist\\n   The 17 Best Austin Restaurants for Vegans and Vegetarians. From decadent mac 'n cheese and mushroom mole to tempeh, we've got you covered.\\n   Source: https://www.thrillist.com/eat/austin/best-vegetarian-and-vegan-restaurants-in-austin-texas\\n\\n2. Find and save ideas about vegan restaurants austin tx on Pinterest.\\n   Best Vegetarian Restaurants In Austin. Vegan Bbq Restaurant Austin.Top Vegan Restaurants in Austin, Texas | Vegan bbq, Vegan restaurants, Vegan. Smothered Potatoes. Cauliflower Buffalo Wings.\\n   Source: https://www.pinterest.com/ideas/vegan-restaurants-austin-tx/924658930251/\\n\\n3. The 16 Best Vegan and Vegetarian Restaurants in Austin, Texas\\n   We love our veggies. And our vegan Frito pie. Food Republic, Sept. 2012.\\n   Source: https://www.megangiller.com/vegan-vegetarian-restaurants-austin\\n\", \"type\": \"tool\", \"name\": \"web_search\", \"tool_call_id\": \"toolu_bdrk_01C7iti2bBH75cZ22mTfuyAv\", \"status\": \"success\"}}, \"kwargs\": {\"tags\": [\"seq:step:1\"], \"color\": \"green\", \"name\": \"web_search\"}}",
                    "role": "assistant"
                }
            ]
        },
        "input": {
            "messages": [
                {
                    "content": "{\"input_str\": \"{'query': 'best vegan restaurants Austin Texas'}\", \"tags\": [\"seq:step:1\"], \"metadata\": {\"ls_integration\": \"langchain_create_agent\", \"langgraph_step\": 2, \"langgraph_node\": \"tools\", \"langgraph_triggers\": [\"__pregel_push\"], \"langgraph_path\": [\"__pregel_push\", 0, false], \"langgraph_checkpoint_ns\": \"tools:9b7a0ff6-af26-ae60-8d6a-6d488a7bff7e\", \"checkpoint_ns\": \"tools:9b7a0ff6-af26-ae60-8d6a-6d488a7bff7e\"}, \"inputs\": {\"query\": \"best vegan restaurants Austin Texas\"}, \"kwargs\": {\"color\": \"green\", \"name\": null, \"tool_call_id\": \"toolu_bdrk_01C7iti2bBH75cZ22mTfuyAv\"}}",
                    "role": "user"
                }
            ]
        }
    },
    "attributes": {
        "event.name": "opentelemetry.instrumentation.langchain",
        "session.id": "83846d05-5b20-4fd5-aaf6-72b52f8c96e0"
    },
    "flags": 1,
    "traceId": "69e7f4137f7ae6e841baf36e4b354344",
    "spanId": "acfb14ebaa01bbcd"
}
{
    "resource": {
        "attributes": {
            "deployment.environment.name": "bedrock-agentcore:default",
            "aws.local.service": "langgraph_rt_obsy_demo.DEFAULT",
            "service.name": "langgraph_rt_obsy_demo.DEFAULT",
            "cloud.region": "us-east-1",
            "aws.log.stream.names": "otel-rt-logs",
            "telemetry.sdk.name": "opentelemetry",
            "aws.service.type": "gen_ai_agent",
            "telemetry.sdk.language": "python",
            "cloud.provider": "aws",
            "cloud.resource_id": "arn:aws:bedrock-agentcore:us-east-1:467801433859:runtime/langgraph_rt_obsy_demo-W2asBi97E7/runtime-endpoint/DEFAULT:DEFAULT",
            "aws.log.group.names": "/aws/bedrock-agentcore/runtimes/langgraph_rt_obsy_demo-W2asBi97E7-DEFAULT",
            "telemetry.sdk.version": "1.40.0",
            "cloud.platform": "aws_bedrock_agentcore",
            "telemetry.auto.version": "0.17.0-aws"
        }
    },
    "scope": {
        "name": "opentelemetry.instrumentation.botocore.bedrock-runtime",
        "schemaUrl": "https://opentelemetry.io/schemas/1.30.0"
    },
    "timeUnixNano": 0,
    "observedTimeUnixNano": 1776808993619475646,
    "severityNumber": 0,
    "severityText": "",
    "body": {
        "content": "1. Best Vegetarian and Vegan Restaurants in Austin to Try... - Thrillist\n   The 17 Best Austin Restaurants for Vegans and Vegetarians. From decadent mac 'n cheese and mushroom mole to tempeh, we've got you covered.\n   Source: https://www.thrillist.com/eat/austin/best-vegetarian-and-vegan-restaurants-in-austin-texas\n\n2. Find and save ideas about vegan restaurants austin tx on Pinterest.\n   Best Vegetarian Restaurants In Austin. Vegan Bbq Restaurant Austin.Top Vegan Restaurants in Austin, Texas | Vegan bbq, Vegan restaurants, Vegan. Smothered Potatoes. Cauliflower Buffalo Wings.\n   Source: https://www.pinterest.com/ideas/vegan-restaurants-austin-tx/924658930251/\n\n3. The 16 Best Vegan and Vegetarian Restaurants in Austin, Texas\n   We love our veggies. And our vegan Frito pie. Food Republic, Sept. 2012.\n   Source: https://www.megangiller.com/vegan-vegetarian-restaurants-austin\n",
        "id": "toolu_bdrk_01C7iti2bBH75cZ22mTfuyAv"
    },
    "attributes": {
        "gen_ai.system": "aws.bedrock"
    },
    "flags": 1,
    "traceId": "69e7f4137f7ae6e841baf36e4b354344",
    "spanId": "7181370e6f3c8b41"
}
{
    "resource": {
        "attributes": {
            "deployment.environment.name": "bedrock-agentcore:default",
            "aws.local.service": "langgraph_rt_obsy_demo.DEFAULT",
            "service.name": "langgraph_rt_obsy_demo.DEFAULT",
            "cloud.region": "us-east-1",
            "aws.log.stream.names": "otel-rt-logs",
            "telemetry.sdk.name": "opentelemetry",
            "aws.service.type": "gen_ai_agent",
            "telemetry.sdk.language": "python",
            "cloud.provider": "aws",
            "cloud.resource_id": "arn:aws:bedrock-agentcore:us-east-1:467801433859:runtime/langgraph_rt_obsy_demo-W2asBi97E7/runtime-endpoint/DEFAULT:DEFAULT",
            "aws.log.group.names": "/aws/bedrock-agentcore/runtimes/langgraph_rt_obsy_demo-W2asBi97E7-DEFAULT",
            "telemetry.sdk.version": "1.40.0",
            "cloud.platform": "aws_bedrock_agentcore",
            "telemetry.auto.version": "0.17.0-aws"
        }
    },
    "scope": {
        "name": "opentelemetry.instrumentation.botocore.bedrock-runtime",
        "schemaUrl": "https://opentelemetry.io/schemas/1.30.0"
    },
    "timeUnixNano": 0,
    "observedTimeUnixNano": 1776808993619455618,
    "severityNumber": 0,
    "severityText": "",
    "body": {
        "content": [
            {
                "name": "web_search",
                "input": {
                    "query": "best vegan restaurants Austin Texas"
                },
                "id": "toolu_bdrk_01C7iti2bBH75cZ22mTfuyAv",
                "type": "tool_use"
            }
        ],
        "tool_calls": [
            {
                "type": "function",
                "id": "toolu_bdrk_01C7iti2bBH75cZ22mTfuyAv",
                "function": {
                    "name": "web_search",
                    "arguments": {
                        "query": "best vegan restaurants Austin Texas"
                    }
                }
            }
        ]
    },
    "attributes": {
        "gen_ai.system": "aws.bedrock"
    },
    "flags": 1,
    "traceId": "69e7f4137f7ae6e841baf36e4b354344",
    "spanId": "7181370e6f3c8b41"
}
```