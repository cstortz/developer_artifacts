LLM Prompt Template
=================

This template provides guidance for LLMs to follow the project structure and documentation requirements.

Project Structure Guidelines
-------------------------

When creating or modifying code, follow these guidelines:

1. **Directory Structure**:
   - Place API endpoints in `src/api/endpoints/`
   - Place data models in `src/models/`
   - Place business logic in `src/services/`
   - Place utility functions in `src/utils/`
   - Place database models in `src/db/`
   - Place core functionality in `src/core/`

2. **File Naming**:
   - Use snake_case for Python files
   - Use descriptive names that indicate purpose
   - Group related endpoints in separate files

3. **Code Organization**:
   - Keep files focused and single-purpose
   - Use dependency injection
   - Follow SOLID principles
   - Implement proper error handling
   - Use type hints consistently

TMF Documentation Requirements
---------------------------

For each REST endpoint, include the following TMF-compliant documentation:

1. **API Resource Schema**:
   .. code-block:: json

      {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier"
          },
          "name": {
            "type": "string",
            "description": "Resource name"
          },
          "description": {
            "type": "string",
            "description": "Resource description"
          },
          "status": {
            "type": "string",
            "enum": ["active", "inactive", "pending"],
            "description": "Resource status"
          },
          "createdAt": {
            "type": "string",
            "format": "date-time",
            "description": "Creation timestamp"
          },
          "updatedAt": {
            "type": "string",
            "format": "date-time",
            "description": "Last update timestamp"
          }
        },
        "required": ["id", "name", "status"],
        "additionalProperties": true
      }

2. **API Operation Documentation**:
   .. code-block:: python

      @router.post(
          "/resources",
          response_model=ResourceResponse,
          status_code=201,
          responses={
              400: {"model": ErrorResponse},
              401: {"model": ErrorResponse},
              403: {"model": ErrorResponse},
              409: {"model": ErrorResponse},
              422: {"model": ValidationErrorResponse},
              500: {"model": ErrorResponse}
          },
          summary="Create a new resource",
          description="""
          Creates a new resource with the provided data.
          
          The operation follows TMF 641 Resource Management API specification.
          It validates the input data against the resource schema and ensures
          uniqueness of required fields.
          """,
          tags=["Resources"]
      )
      async def create_resource(
          resource: ResourceCreate,
          current_user: User = Depends(get_current_user)
      ) -> ResourceResponse:
          """
          Create a new resource.
          
          Args:
              resource: Resource data to create
              current_user: Current authenticated user
          
          Returns:
              Created resource with assigned ID
          
          Raises:
              HTTPException: If validation fails or resource creation fails
          """
          pass

3. **API Response Models**:
   .. code-block:: python

      class ResourceResponse(BaseModel):
          """TMF 641 Resource response model."""
          id: str = Field(..., description="Unique identifier")
          name: str = Field(..., description="Resource name")
          description: Optional[str] = Field(None, description="Resource description")
          status: ResourceStatus = Field(..., description="Resource status")
          createdAt: datetime = Field(..., description="Creation timestamp")
          updatedAt: datetime = Field(..., description="Last update timestamp")
          
          class Config:
              schema_extra = {
                  "example": {
                      "id": "res-123",
                      "name": "Example Resource",
                      "description": "An example resource",
                      "status": "active",
                      "createdAt": "2024-03-15T10:00:00Z",
                      "updatedAt": "2024-03-15T10:00:00Z"
                  }
              }

4. **Error Response Models**:
   .. code-block:: python

      class ErrorResponse(BaseModel):
          """TMF Error response model."""
          code: str = Field(..., description="Error code")
          message: str = Field(..., description="Error message")
          details: Optional[Dict[str, Any]] = Field(None, description="Error details")
          
          class Config:
              schema_extra = {
                  "example": {
                      "code": "ERR-001",
                      "message": "Resource not found",
                      "details": {"resourceId": "res-123"}
                  }
              }

5. **API Versioning**:
   - Use URL versioning (e.g., `/api/v1/resources`)
   - Include version in OpenAPI documentation
   - Document breaking changes

6. **API Documentation**:
   - Generate OpenAPI documentation
   - Include example requests and responses
   - Document all possible error scenarios
   - Include authentication requirements

Example Implementation
-------------------

Here's an example of a complete TMF-compliant endpoint implementation:

.. code-block:: python

   from datetime import datetime
   from typing import Optional
   from fastapi import APIRouter, Depends, HTTPException
   from pydantic import BaseModel, Field
   
   router = APIRouter()
   
   class ResourceStatus(str, Enum):
       """Resource status enumeration."""
       ACTIVE = "active"
       INACTIVE = "inactive"
       PENDING = "pending"
   
   class ResourceBase(BaseModel):
       """Base resource model."""
       name: str = Field(..., description="Resource name")
       description: Optional[str] = Field(None, description="Resource description")
       status: ResourceStatus = Field(..., description="Resource status")
   
   class ResourceCreate(ResourceBase):
       """Resource creation model."""
       pass
   
   class ResourceResponse(ResourceBase):
       """Resource response model."""
       id: str = Field(..., description="Unique identifier")
       createdAt: datetime = Field(..., description="Creation timestamp")
       updatedAt: datetime = Field(..., description="Last update timestamp")
       
       class Config:
           schema_extra = {
               "example": {
                   "id": "res-123",
                   "name": "Example Resource",
                   "description": "An example resource",
                   "status": "active",
                   "createdAt": "2024-03-15T10:00:00Z",
                   "updatedAt": "2024-03-15T10:00:00Z"
               }
           }
   
   @router.post(
       "/resources",
       response_model=ResourceResponse,
       status_code=201,
       responses={
           400: {"model": ErrorResponse},
           401: {"model": ErrorResponse},
           403: {"model": ErrorResponse},
           409: {"model": ErrorResponse},
           422: {"model": ValidationErrorResponse},
           500: {"model": ErrorResponse}
       },
       summary="Create a new resource",
       description="""
       Creates a new resource with the provided data.
       
       The operation follows TMF 641 Resource Management API specification.
       It validates the input data against the resource schema and ensures
       uniqueness of required fields.
       """,
       tags=["Resources"]
   )
   async def create_resource(
       resource: ResourceCreate,
       current_user: User = Depends(get_current_user)
   ) -> ResourceResponse:
       """
       Create a new resource.
       
       Args:
           resource: Resource data to create
           current_user: Current authenticated user
       
       Returns:
           Created resource with assigned ID
       
       Raises:
           HTTPException: If validation fails or resource creation fails
       """
       try:
           # Validate resource data
           if await resource_service.exists_by_name(resource.name):
               raise HTTPException(
                   status_code=409,
                   detail={
                       "code": "ERR-002",
                       "message": "Resource with this name already exists",
                       "details": {"name": resource.name}
                   }
               )
           
           # Create resource
           created_resource = await resource_service.create(
               resource=resource,
               user_id=current_user.id
           )
           
           return ResourceResponse.from_orm(created_resource)
           
       except ValidationError as e:
           raise HTTPException(
               status_code=422,
               detail={
                   "code": "ERR-003",
                   "message": "Validation error",
                   "details": e.errors()
               }
           )
       except Exception as e:
           logger.error(f"Failed to create resource: {str(e)}")
           raise HTTPException(
               status_code=500,
               detail={
                   "code": "ERR-004",
                   "message": "Internal server error",
                   "details": {"error": str(e)}
               }
           ) 