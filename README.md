# PullReviewX
A smart Github Action that utilizes Azure OpenAI API to review pull requests, identify  potential issues, and provide actionable feedback.

## Working
![working-diagram](assets/pullreviewx-working.png)

## Installation

#### Setup Actions Workflow
1. Go to `Actions` for you respository
2. Above Search workflows search bar, select the available option to `set up a workflow yourself`
4. In the workflow file editor, please include the snippet below:
```yml
name: Automated PR Review by PullReviewX
on:
  pull_request:
    types: [opened]
jobs:
  review-pr:
    runs-on: ubuntu-latest
    steps:
      - name: PR Review
        uses: kp9435-keril/pull-review-x@<your target version like v1.0.0>
        with:
            GITHUB_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            AZURE_OPENAI_APIKEY: ${{ secrets.AZURE_OPENAI_APIKEY }}
            AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
            AZURE_OPENAI_MODEL: <Your Deployed Model>
            PR_SUMMARY: True
            PR_SUGGEST_CHANGES: True
            PR_COMMENT_SUGGESTED_CHANGES: True
```

#### Setup Azure Secrets
1. Go to `Settings` for your repository
2. Select `Secrets and variables` tab from the sidebar
3. Once the expandable menu opens, Select `Actions`
4. Select `New repository secret`, Add `AZURE_OPENAI_APIKEY` & `AZURE_OPENAI_ENDPOINT`

#### Allow Write Permissions to Workflow
This is required in order to allow workflows to post comments.
1. Go to `Settings` for your repository
2. Select `Actions` tab from the sidebar
3. Once the expandable menu opens, Select `General`
4. Scroll down to `Workflow Permissions` section
5. Select `Read and write permissions`, and click on `Save`

## Usages

1. `PR_SUMMARY`: Whether allow workflow to analyze PR and provide summary in comment. | default: `True`
2. `PR_FAQS`: Whether allow workflow to analyze PR and provide FAQs in comment. | default: `True`
3. `PR_SUGGEST_CHANGES`: Whether allow workflow to analyze PR & suggest changes in comment, if required. | default: `True`
4. `PR_COMMENT_SUGGESTED_CHANGES`: Whether allow workflow to drop review comment in the patch for the suggested changes. | default: `True` 
