# FoldCloud AlphaFold Dashboard

## What's included
- `app.py` — Streamlit app with live AlphaFold Database lookup and interactive 3Dmol.js viewer.
- `html_pages/structure_search.html` — supplied Structure Search & 3D Viewer UI.
- `html_pages/batch_prediction.html` — supplied Batch Prediction UI.
- `html_pages/cloud_architecture.html` — supplied Cloud Architecture UI.
- `html_pages/saved_structures.html` — supplied Saved Structures & Catalog UI.

## Run on Windows
1. Extract this ZIP file.
2. Open the extracted folder in VS Code.
3. Open Terminal in VS Code.
4. Install dependencies:
   ```bash
   pip install streamlit requests
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Notes
- The default **Live Protein Search** page retrieves live records from the AlphaFold Database.
- Average confidence first uses AlphaFold's `confidenceAvgLocalScore`. If absent, the app calculates mean pLDDT from the B-factor column in the downloaded AlphaFold PDB file. If neither is available, it displays `Not provided by AlphaFold` rather than inventing a score.
- The four HTML dashboard pages are your supplied designs. Select a page in the Streamlit navigation and enter a UniProt accession in the sidebar; the page is populated with live AlphaFold accession, protein name, gene, sequence length, and confidence data. AWS execution metrics and job controls remain visual product-design elements until an AWS prediction service is configured.
- Google Fonts, Tailwind CDN, and 3Dmol.js require internet access.
