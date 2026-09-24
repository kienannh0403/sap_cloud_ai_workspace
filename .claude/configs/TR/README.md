# TR — Treasury (Public Cloud: FIN-FSCM-TRM, cash management)

Sub-areas: financial transactions (money market, FX, derivatives, securities), hedge management, market risk (NPV).
Cash / liquidity management and bank accounts sit in FIN-FSCM-CLM (not covered here). Replaces sc4sap `configs/TR/`
(FTR_CREATE, VTB* tables).

Legend **R / C / f / u**: see `configs/FI/README.md`.

## Read — CDS views

| Views | Evidence |
|---|---|
| `I_FinancialTransaction`, `I_FinancialPosition`, `I_HedgingRelationship` | C |
| `I_FinTransFlow`, `I_FinTransCondition`, `I_FinTransNominal`, `I_FinancialTransactionNPV`, `I_HedgedItem`, `I_HedgingInstrument`, `I_FTR_Counterparty` | R |
| Code lists: `I_FinancialInstrProductType`, `I_FinInstrTransCat`, `I_FinTransFlowType` (+ `…Text`) | R |

Deprecated (use successor): `I_FinTransFlowPostgBlkgRsn` → `I_FinTransFlowFixingBlkgRsn`, `I_FinTransFlowPostgStatus`
→ `I_FinTransFlowFixingStatus`, `I_VolatilityProfile` → `I_VolatilityProfile_2`.

## Write — RAP BOs (EML), all R

`I_FinTransIntrstRateInstrTP` (+ `D_IntrstRateInstrChangeP`), `I_FinancialTransactionNPVTP`.

## Notes

- Counterparty / bank data is blocklisted for row reads (`exceptions/banking-payment.md`).
- `I_BankAccount`, `I_CashFlow`, `I_CashPositionRawData` were not found — cash management needs its own lookup.
- Catalog folder `FIN/` (FIN-FSCM, 196 views). Key-user config: all **u**.
