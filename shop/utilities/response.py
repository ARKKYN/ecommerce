from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
import json
from uuid import UUID

def parse_json_strings(data):
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
    elif isinstance(data, dict):
        return {k: parse_json_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parse_json_strings(item) for item in data]
    elif isinstance(data, UUID):
        return str(data)
    elif hasattr(data, '__dict__'):
        return parse_json_strings(dict(data))
    return data

def ok_response(data, status_code: int = HTTP_200_OK):
    parsed_data = parse_json_strings(data)
    return JSONResponse(status_code=status_code, content={"success": True, "data": parsed_data})

def error_response(message: str, status_code: int = HTTP_500_INTERNAL_SERVER_ERROR, errors = None):
  body = {"success": False, "message": message,"data": {}}
  if errors:
    body["errors"] = errors
  return JSONResponse(status_code=status_code, content=body)

