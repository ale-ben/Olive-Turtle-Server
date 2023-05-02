::: mermaid
graph TD;
	classDef userInput  fill:#2a5279, color:#ffffff, stroke:#ffffff
    classDef state fill:#222222, color:#ffffff, stroke:#ffffff
    classDef entryPoint fill:#009c11, stroke:#42FF57, color:#ffffff
    classDef termination fill:#bb0007, stroke:#E60109, color:#ffffff
    START(("/start")):::entryPoint --> AUTH{User ID / Chat ID valid?};
	AUTH --> |No| AUTHFAIL[Auth denied];
	AUTH --> |Yes| SELECTACT((Select action)):::state;
	AUTHFAIL --> |Print User ID\n and Chat ID| AUTHFAILEND((End)):::termination;
	SELECTACT --> |/devlist| SELECTDEV((Select device)):::state;
	SELECTACT -->  |/permissions| MANAGEPERM((Manage permissions)):::state;
	SELECTDEV --> |Print device\n list| SELECTDEVCHOICE("(choice)"):::userInput
	SELECTDEVCHOICE -->  DEVMENU((Device menu));
	

:::