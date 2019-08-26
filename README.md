# Config Compliance Automation Service v1.0.0
A network automation service that checks compliance of network device based on compliance policies
configured in the config policy API.
- Multi-vendor support
- Device Inventory API
- Config Policy API
- Template Renderer
- Log files output to easily determine what configs are not deployed to specific devices

## Workflow
![Alt Text](Workflow.png?raw=True)

## Running the Workflow
- Deploy the topology
<code>make deploy</code>
- Run the compliance checker
<code>make run</code>
    - Requires the compliance/device API to be running
    - Device topology must be deployed
- Cleanup and Teardown
<code>make cleanup</code>

## API Endpoints
|      Endpoint                 |  Method  |       Purpose             |
|-------------------------------|----------|---------------------------|
|/api/v1/devices/               | GET      | Retrieves all devices     |
|/api/v1/devices/{device}/      | GET      | Retrieves a device        |
|/api/v1/config/compliance/     | GET/POST | Retrieves/adds a policy   |
|/api/v1/config/compliance/{id}/| GET      | Retrieves a policy by id  |
