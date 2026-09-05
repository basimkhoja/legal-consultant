# CA chain for laws.boe.gov.sa

`boe-chain.pem` holds two public certificates, nothing else:

1. DigiCert Global G2 TLS RSA SHA256 2020 CA1 (intermediate), downloaded on
   2026-09-05 from
   `https://cacerts.digicert.com/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt.pem`.
2. DigiCert Global Root G2 (root), copied from macOS `/etc/ssl/cert.pem`.

Why it exists: the Bureau of Experts portal serves its leaf certificate without
the intermediate. macOS `curl` completes the chain from the system trust store,
but inside an agent sandbox that blocks the Keychain (OpenAI Codex CLI's
seatbelt sandbox, for one) verification fails with `curl: (60)`.
`scripts/fetch-law.py` tries the default verification first and uses this file
only when that fails with exit code 60.

To refresh: re-download the intermediate, extract the root with
`awk '/DigiCert Global Root G2/{f=1} f&&/BEGIN CERT/{p=1} p{print} p&&/END CERT/{exit}' /etc/ssl/cert.pem`,
concatenate, and check with
`openssl crl2pkcs7 -nocrl -certfile boe-chain.pem | openssl pkcs7 -print_certs -noout`.
The intermediate expires 2031-03-29.
