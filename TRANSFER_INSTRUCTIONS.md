# Transfer repository instructions

Follow these steps to transfer the repository `jacejuice222014-droid/Jace` to the new owner `baskhopper-hoop`.

API (curl) method:

1. Create a Personal Access Token (PAT) with the `repo` scope. Do NOT share this token.
2. Replace YOUR_PERSONAL_ACCESS_TOKEN in the command below with your PAT and run it locally.

curl -X POST -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN" \
  https://api.github.com/repos/jacejuice222014-droid/Jace/transfer \
  -d '{"new_owner":"baskhopper-hoop"}'

Web UI method:

1. Sign in to GitHub as `jacejuice222014-droid`.
2. Open the repo: https://github.com/jacejuice222014-droid/Jace
3. Click Settings → scroll to Danger Zone → Transfer
4. Enter the repository name to confirm: `jacejuice222014-droid/Jace`
5. Enter new owner: `baskhopper-hoop` and confirm.

Notes:
- If `baskhopper-hoop` already has a repo named `Jace`, rename your repo first.
- The recipient may need to accept or have permissions in their organization.

