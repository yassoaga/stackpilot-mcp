# Sources and licenses

This repository contains the StackPilot MCP server code and its documentation. It does not contain a copy of any of the lists below: no database, no data files. An index built from these lists contains their material, and each source keeps its own license.

## Indexed by default

| Source | License | Copyright notice |
|---|---|---|
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | MIT | Copyright (c) 2024 Frank Fiegel |
| [f/prompts.chat](https://github.com/f/prompts.chat) | Prompt texts: CC0 1.0. Code: MIT | Copyright (c) 2022-present Fatih Kadir Akin and contributors |
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | MIT | Copyright (c) 2022 public-apis |
| [awesome-selfhosted/awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) | CC BY-SA 3.0 | — (no copyright line in LICENSE) |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | CC0 1.0 | — |

- MIT: https://opensource.org/licenses/MIT
- CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/
- CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/ — this license requires attribution and ShareAlike. An index that contains awesome-selfhosted material and is shared with others must keep those terms.

## Excluded sources

| Source | Reason |
|---|---|
| [ripienaar/free-for-dev](https://github.com/ripienaar/free-for-dev) | The repository has no license file and no license statement, so all rights are reserved by default. |
| [DigitalPlatDev/FreeDomain](https://github.com/DigitalPlatDev/FreeDomain) | GNU AGPL-3.0. StackPilot does not redistribute it. |

`mcp_hub_server.py` drops results from these two sources by default and leaves them out of `hub_stats`. The `STACKPILOT_EXCLUDE_SOURCES` environment variable (comma-separated source names) replaces the default list. If you build your own index locally from lists you choose, you are responsible for each list's license.

## Other notes

The MCP server code and documentation in this repository are by Base of AGI. Third-party listings remain the property of their owners; check each service's own terms before use.

License information was taken from each source repository's LICENSE file or README license section (checked 2026-10-20).
