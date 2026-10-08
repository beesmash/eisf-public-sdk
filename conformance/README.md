# EISf Conformance Suite v0.1

The conformance suite defines a public minimum bar for claiming **EISf Core Compatible**.

## Mandatory claim

An implementation that passes all mandatory fixtures may state:

> **EISf Core Compatible — Self-Tested against EISf Conformance Suite v0.1**

Do not remove **Self-Tested** unless an independent certification process actually evaluated the implementation.

## Driver protocol

Run:

```bash
eisf conformance --driver "your-tool eisf-driver"
```

For each fixture, the suite invokes the driver and sends one JSON document on standard input:

```json
{"operation":"validate","case":{...}}
```

The driver MUST return JSON on standard output.

Valid response:

```json
{"valid":true,"case":{...},"errors":[]}
```

Invalid response:

```json
{"valid":false,"errors":["reason"]}
```

For a valid fixture, `case` MUST be a JSON object that can be exposed as the implementation's portable EISf case.

Conformance tests interoperability with the public core. It is not a security, accuracy, quality, or JANUS certification.
