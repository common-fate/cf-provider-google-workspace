<p align="center"><img src="https://static.commonfate.io/logos/commonfate/screen/light_purple/common_fate_logo_light_purple.svg" height="40" /></p>

<h1 align="center">Common Fate Google Workspace Provider</h1>

<p align="center">An <a href="https://docs.commonfate.io/common-fate/providers/providers">Access Provider</a> for automating permissions to Google Workspace.</p>

<p align="center">
<a align="center"  href="https://join.slack.com/t/commonfatecommunity/shared_invite/zt-q4m96ypu-_gYlRWD3k5rIsaSsqP7QMg"><img src="https://img.shields.io/badge/slack-commonfate-1F72FE.svg?logo=slack" alt="slack" /></a>
</p>
<br/>

## Access

This Access Provider provisions a temporary Google Workspace Group assignment. You can use this in conjunction with SAML applications to allow users to request elevated access to SaaS applications.

This Access Provider uses the following permission scopes:

- `https://www.googleapis.com/auth/admin.directory.group`
- `https://www.googleapis.com/auth/admin.directory.group.member`

## Getting started

### Prerequisites

To use this Access Provider you'll need to have [deployed Common Fate](https://docs.commonfate.io/common-fate/next/deploying-common-fate/deploying-common-fate). You'll also need to [download the `cf` CLI](https://docs.commonfate.io/common-fate/next/providers/setup).

You will also need AWS credentials with the ability to deploy CloudFormation templates.

### 1. Generate credentials

You'll need to create some credentials in Google Workspace to configure this pro

#### Customer ID

_Used as `customer_id`_

In your Google Admin console (at admin.google.com)...
Go to Menu and navigate to Account > Account settings > Profile.
Next to Customer ID, find your organization's unique ID.

#### Admin Email

_Used as `admin_email`_

Provide the email of a Google Workspace administrator. If you like, you can create a dedicated email address for this Access Provider to use, such as `cf-google-workspace-provider@example.com`.

#### Credentials

_Used as `credentials_base64`_

The below instructions have been taken from [Google's documentation on creating a Service Account](https://developers.google.com/workspace/guides/create-credentials#service-account).

The service account requires domain-wide delegation in order to manage group membership. Only the Google Workspace access provider will have access to these credentials (not Common Fate, nor any users using Common Fate). Make sure to keep the service account credentials safe and delete any copies from your computer after deploying this Access Provider.

In the Google Cloud console, go to IAM & Admin > Service Accounts.

Go to Service Accounts

Click Create service account.

Fill in the service account details, then click Create and continue.

Click Done.

Select your service account.

Click Keys > Add key > Create new key.

Select JSON, then click Create.

Your new public/private key pair is generated and downloaded to your machine as a new file. This file is the only copy of this key. For information about how to store your key securely, see Managing service account keys.

Click Close.

**Set up domain-wide delegation for a service account**
To call APIs on behalf of users in a Google Workspace organization, your service account needs to be granted domain-wide delegation of authority in the Google Workspace Admin console by a super administrator account. For more information, see [Delegating domain-wide authority to a service account](https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority).
To set up domain-wide delegation of authority for a service account:

In the Google Cloud console, go to Menu menu > IAM & Admin > Service Accounts.

Go to Service Accounts

Select your service account.

Click Show advanced settings.

Under "Domain-wide delegation," find your service account's "Client ID." Click Copy to copy the client ID value to your clipboard.

If you have super administrator access to the relevant Google Workspace account, click View Google Workspace Admin Console, then sign in using a super administrator user account and continue following these steps.

If you don't have super administrator access to the relevant Google Workspace account, contact a super administrator for that account and send them your service account's Client ID and list of OAuth Scopes so they can complete the following steps in the Admin console.

In the Google Admin console, go to Menu menu > Security > Access and data control > API controls.

Go to API controls

Click Manage Domain Wide Delegation.

Click Add new.

In the "Client ID" field, paste the client ID you copied in step 5.

In the "OAuth Scopes" field, enter a comma-delimited list of the scopes required by your application. This is the same set of scopes you defined when configuring the OAuth consent screen.

Click Authorize.

### 2. Deploy the Access Provider

To deploy this Access Provider, open a terminal window and assume an AWS role with access to deploy CloudFormation resources in the Common Fate account. Then, run:

```
cf provider deploy
```

and select the `common-fate/cloudwatch-log-groups` Provider when prompted.
