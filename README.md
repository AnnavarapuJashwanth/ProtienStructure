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

## Deploy on AWS EC2

The repository includes an EC2 service definition and an Ubuntu user-data
script in [`deploy/`](./deploy/).

### Option 1: Automatic setup with EC2 user data

1. Open **EC2 → Launch instance** in the AWS Console.
2. Select Ubuntu Server 24.04 LTS.
3. Use an instance size with at least 2 GB RAM, such as `t3.small`.
4. Create or select a key pair for SSH access.
5. In the security group, allow:
   - SSH (TCP `22`) from **My IP** only.
   - Custom TCP (TCP `8501`) from **My IP** for testing.
6. In **Advanced details → User data**, paste the contents of
   [`deploy/ec2-user-data.sh`](./deploy/ec2-user-data.sh).
7. Launch the instance and wait for the setup to finish.
8. Open `http://INSTANCE_PUBLIC_IP:8501`.

For a public production deployment, do not leave port `8501` open to the
whole internet. Put Nginx or an AWS load balancer in front of Streamlit,
serve it over HTTPS, and restrict the instance security group to the proxy.

### Option 2: Manual setup over SSH

```bash
sudo apt-get update
sudo apt-get install -y git python3-venv python3-pip
sudo git clone --branch main https://github.com/AnnavarapuJashwanth/ProtienStructure.git /opt/foldcloud
sudo python3 -m venv /opt/foldcloud/.venv
sudo /opt/foldcloud/.venv/bin/pip install -r /opt/foldcloud/requirements.txt
sudo cp /opt/foldcloud/deploy/foldcloud.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now foldcloud.service
```

Check the service with:

```bash
sudo systemctl status foldcloud
sudo journalctl -u foldcloud -f
```

## Notes
- The default **Live Protein Search** page retrieves live records from the AlphaFold Database.
- Average confidence first uses AlphaFold's `confidenceAvgLocalScore`. If absent, the app calculates mean pLDDT from the B-factor column in the downloaded AlphaFold PDB file. If neither is available, it displays `Not provided by AlphaFold` rather than inventing a score.
- The four HTML dashboard pages are your supplied designs. Select a page in the Streamlit navigation and enter a UniProt accession in the sidebar; the page is populated with live AlphaFold accession, protein name, gene, sequence length, and confidence data. AWS execution metrics and job controls remain visual product-design elements until an AWS prediction service is configured.
- Google Fonts, Tailwind CDN, and 3Dmol.js require internet access.
