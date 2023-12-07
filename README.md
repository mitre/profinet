# MITRE Caldera™ for OT plugin: Profinet

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying [MITRE Caldera™](https://github.com/mitre/caldera) with Profinet protocol TTPs mapped to MITRE ATT&CK® for ICS [v14](https://attack.mitre.org/resources/updates/updates-october-2023/). This is part of a series of plugins that provide added threat emulation capability for Operational Technology (OT) environments.

Currently this plugin provides coverage for functions within the __Profinet Discovery and Basic Configuration Protocol__ (DCP) service. DCP supports configuration of Profinet devices via link-layer communications. Profinet devices typically use DCP on system start-up to identify network addresses of target endpoints.

Full Profinet plugin [documentation](docs/profinet.md) can be viewed as part of fieldmanual, once the Caldera server is running.

## Installation

To run Caldera along with Profinet plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install the Profinet plugin in Caldera's plugin directory: `caldera/plugins`
3. Enable the Profinet plugin by adding `- profinet` to the list of enabled plugins in `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure mode)

### Version
This plugin is compatible with the current version of Caldera v4.2.0 as of 8 Dec 2023. This can be checked out using the following method:
```
git clone --recursive https://github.com/mitre/caldera.git
```
### Tested OS Versions for Plugin Payload(s)

Building of the Profinet plugin payloads has been tested as described [here](/src/README.md#reproducing-builds). See the corresponding plugin payload source code for further build information.

Testing of the binaries has occured on:
* Microsoft Windows 10 v21H2
* Ubuntu 22.04.2 LTS

#### Plugin Payload Source Code

For additional information on the Profinet plugin payload source code, please see [this corresponding repository](/src/), which contains additional licensing and build guidance.

## Plugin Usage
 - Import the plugin, and optionally set up the required facts. Simplest method is to create a source with the Caldera UI.
 - Start an operation, optionally using the fact source you set up.
 - Use "Add Potential Link" to run a specific ability from this plugin. You can enter the fact values manually, or use the ones from your fact source.
