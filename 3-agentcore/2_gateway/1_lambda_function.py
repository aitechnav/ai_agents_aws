import json

def lambda_handler(event, context):
    """
    Lambda function that handles multiple tools via Bedrock Agent Core Gateway
    
    Agent Core passes tool information via context.client_context.custom with:
    - bedrockAgentCoreToolName: Full tool name with prefix (e.g., "WeatherAndTimeTools___get_weather")
    - bedrockAgentCoreTargetId: Target ID from gateway
    - bedrockAgentCoreGatewayId: Gateway ID
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Get tool name from client context (set by Agent Core Gateway)
    tool_name = 'unknown'
    
    # Agent Core passes tool info in client context
    if context.client_context is not None and hasattr(context.client_context, 'custom'):
        full_tool_name = context.client_context.custom.get('bedrockAgentCoreToolName', 'unknown')
        print(f"Full tool name from Agent Core: {full_tool_name}")
        
        # Strip the prefix - Agent Core adds "TargetName___" automatically
        if '___' in full_tool_name:
            tool_name = full_tool_name.split('___')[1]
        else:
            tool_name = full_tool_name
    
    # Fallback: Allow tool_name to be passed in event for direct testing
    if 'tool_name' in event:
        tool_name = event['tool_name']
    
    print(f"Determined tool name: {tool_name}")
    
    # Handle weather tool
    if tool_name == 'get_weather':
        location = event.get('location', 'Unknown')
        return {
            'statusCode': 200,
            'body': json.dumps({
                'location': location,
                'temperature': 72,
                'conditions': 'Partly cloudy',
                'humidity': 65
            })
        }
    
    # Handle time tool  
    elif tool_name == 'get_time':
        timezone = event.get('timezone', 'UTC')
        return {
            'statusCode': 200,
            'body': json.dumps({
                'timezone': timezone,
                'time': '2025-09-02 15:00:00'
            })
        }
    
    # Handle unknown tools
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': f'Unknown tool: {tool_name}',
                'debug_info': {
                    'received_event': event,
                    'available_tools': ['get_weather', 'get_time']
                }
            })
        }
