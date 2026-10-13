This is the CI/CD from the project named Crusource VMS (Vendor management system), the project that I am working is Crusource CRM (Coustomer releation management). but i want to implement this CI/CD in my project, and it has to be based on my project. that is why i have pasted this CI/CD of theire project here. Remeber this is just the sample for your refference. and things can be different in AWS, so what are all the informtion you want to make a CI/CD file for my project, give me a list which I can send to my team lead who manages the AWS. 

Backend:
CI:
name: CI

on:
  pull_request:
    branches: [dev, stage, main]
  push:
    branches: [dev, stage, main]

# Cancel superseded runs on force-push / new commits to the same PR
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  # Kept at 20 to match actual production/dev runtime. Don't bump this to
  # 22 just because @types/node or an LTS schedule suggests it — that's a
  NODE_VERSION: '22'

jobs:
  # ---------------------------------------------------------------------------
  # Fan-out stage: fast, independent checks, run in parallel.
  # No shared install job — GitHub Actions jobs run on separate fresh
  # runners, so a prior job's node_modules isn't visible to later jobs
  # anyway. Each job below does its own checkout + setup-node + npm ci,
  # and setup-node's cache: npm keeps that fast (~5-10s on a cache hit
  # instead of a full re-download).
  # ---------------------------------------------------------------------------

  lint:
    name: Lint (ESLint)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  format:
    name: Format check (Prettier)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run format:check

  build:
    name: Build (TypeScript)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run build

      # Groundwork for a future deploy job — not consumed by anything yet.
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 3

  security-scan:
    name: Security audit (npm audit)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      # audit-level=high: only fail on high/critical, per your call above.
      # continue-on-error: true for now — this makes findings VISIBLE on
      # every PR without blocking merges, while the current vulnerability
      # backlog gets triaged. Once you've either fixed or built an
      # allowlist for accepted-risk transitive deps (e.g. via audit-ci
      # + .audit-ci.jsonc), remove continue-on-error to make this a real gate.
      - name: Run npm audit (high/critical only, report-only for now)
        run: npm audit --audit-level=high
        continue-on-error: true
            
  migration-drift-check:
    name: Migration drift check
    runs-on: ubuntu-latest
    needs: [lint, format, build, security-scan]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Copy .env.test to .env
        run: cp .env.test .env

      - name: Generate migrations and check for drift
        env:
          MIGRATIONS_DIR: ./src/libs/infrastructure/database/migrations
        run: |
          npm run db:generate # ASSUMPTION: your existing Drizzle Kit generate script name
          if [ -n "$(git status --porcelain "$MIGRATIONS_DIR")" ]; then
            echo "::error::Uncommitted schema drift detected. Run 'npm run db:generate' locally and commit the migration."
            git status --porcelain "$MIGRATIONS_DIR"
            git diff "$MIGRATIONS_DIR"
            exit 1
          fi

  e2e-test:
    name: E2E tests
    runs-on: ubuntu-latest
    needs: [lint, format, build, security-scan]
    timeout-minutes: 40
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: crusource_test
        ports:
          - 5432:5432
        # Health check closes the classic "port open, not accepting
        # connections yet" gap that causes flaky first-run e2e failures.
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10


    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci

      - name: Copy .env.test to .env
        run: cp .env.test .env

      - name: Wait for Postgres
        run: |
          until pg_isready -h localhost -p 5432 -U postgres; do
            echo "Waiting for postgres..."
            sleep 2
          done

      - name: Enable pgvector extension
        run: PGPASSWORD=postgres psql -h localhost -U postgres -d crusource_test -c "CREATE EXTENSION IF NOT EXISTS vector;"

      - name: Push Database Schema
        run: npm run db:migrate

      - name: Apply Row Level Security Policies
        run: npx ts-node -r tsconfig-paths/register src/libs/infrastructure/database/apply-rls.ts

      - name: Run E2E tests
        run: npm run test:e2e -- --runInBand
        # --runInBand kept: prevents concurrent workers from hitting
        # transaction/RLS locking issues against the same test database.

  # ---------------------------------------------------------------------------
  # Optional: PR-title-based conventional commit check.
  # Only include this if you squash-merge PRs (most common on GitHub) — in
  # that case linting individual commit messages is close to useless since
  # they get squashed away, and only the PR title survives into history/changelog.
  # If you merge-commit or rebase-merge instead, replace this with a real
  # commitlint step that walks git log over the PR's commit range.
  # ---------------------------------------------------------------------------
  # pr-title-lint:
  #   name: Conventional commit title check
  #   runs-on: ubuntu-latest
  #   if: github.event_name == 'pull_request'
  #   steps:
  #     - uses: amannn/action-semantic-pull-request@v5
  #       env:
  #         GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
CD:

name: Deploy Backend to Production

on:
  workflow_run:
    workflows: ["CI"]
    branches:
      - main
    types:
      - completed

permissions:
  id-token: write
  contents: read

env:
  AWS_REGION: ${{ secrets.PROD_AWS_REGION }}
  ECR_REPOSITORY: ${{ secrets.PROD_ECR_REPOSITORY }}
  ECS_CLUSTER: ${{ secrets.PROD_ECS_CLUSTER }}
  ECS_SERVICE: ${{ secrets.PROD_ECS_SERVICE }}
  ECS_TASK_DEFINITION: ${{ secrets.PROD_ECS_TASK_DEFINITION }}
  CONTAINER_NAME: ${{ secrets.PROD_CONTAINER_NAME }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Checkout Source
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha }}

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Build Application
        run: npm run build

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.PROD_AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build Docker Image
        run: |
          docker build \
            --target api \
            -t $ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }} \
            -t $ECR_REPOSITORY:production \
            .

      - name: Build Migrator Image
        run: |
          docker build \
            --target migrator \
            -t $ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }} \
            .

      - name: Tag Images
        run: |
          docker tag \
          $ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }} \
          ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }}

          docker tag \
          $ECR_REPOSITORY:production \
          ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:production

          docker tag \
          $ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }} \
          ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }}

      - name: Push Docker Images
        run: |
          docker push ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }}
          docker push ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:production
          docker push ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }}

      - name: Prepare Migration Task Definition
        run: |
          # run-task's containerOverrides does NOT support overriding "image"
          # (only name, command, environment, environmentFiles, cpu, memory,
          # memoryReservation, resourceRequirements are allowed). So we register
          # a dedicated task definition revision that already points at the
          # migrator image, and run that revision instead.
          aws ecs describe-task-definition \
            --task-definition $ECS_TASK_DEFINITION \
            --query taskDefinition \
            > base-task-definition.json

          MIGRATOR_IMAGE="${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }}"
          LOG_GROUP="/ecs/crusource-prod-migrator"
          REGION="${{ env.AWS_REGION }}"

          # Inject the migrator image AND force a dedicated awslogs logConfiguration
          # so that ALL migrator output is always captured in CloudWatch, regardless
          # of what the base task definition has.
          jq --arg IMAGE "$MIGRATOR_IMAGE" \
             --arg NAME "$CONTAINER_NAME" \
             --arg LOG_GROUP "$LOG_GROUP" \
             --arg REGION "$REGION" '
            .containerDefinitions = (.containerDefinitions | map(
              if .name == $NAME then
                .image = $IMAGE |
                .logConfiguration = {
                  "logDriver": "awslogs",
                  "options": {
                    "awslogs-group": $LOG_GROUP,
                    "awslogs-region": $REGION,
                    "awslogs-stream-prefix": "ecs",
                    "awslogs-create-group": "true"
                  }
                }
              else . end
            )) |
            del(.taskDefinitionArn, .revision, .status, .requiresAttributes,
                .compatibilities, .registeredAt, .registeredBy)
          ' base-task-definition.json > migration-task-definition.json

          echo "=== Migration task definition (container defs) ==="
          jq '.containerDefinitions[] | {name, image, logConfiguration}' migration-task-definition.json

          MIGRATION_TASK_DEF_ARN=$(aws ecs register-task-definition \
            --cli-input-json file://migration-task-definition.json \
            --query 'taskDefinition.taskDefinitionArn' \
            --output text)

          echo "Registered migration task definition: $MIGRATION_TASK_DEF_ARN"
          echo "MIGRATION_TASK_DEF_ARN=$MIGRATION_TASK_DEF_ARN" >> $GITHUB_ENV
          echo "MIGRATOR_LOG_GROUP=$LOG_GROUP" >> $GITHUB_ENV

      - name: Create Migrator Log Group
        run: |
          # AmazonECSTaskExecutionRolePolicy only has CreateLogStream + PutLogEvents,
          # NOT CreateLogGroup. Pre-create from here so the migrator container can
          # write logs immediately without needing awslogs-create-group to work.
          aws logs create-log-group \
            --log-group-name "$MIGRATOR_LOG_GROUP" \
            2>&1 | grep -v "ResourceAlreadyExistsException" || true
          echo "Log group ready: $MIGRATOR_LOG_GROUP"

      - name: Run Database Migrations
        env:
          PRIVATE_SUBNET_IDS: ${{ secrets.PROD_PRIVATE_SUBNET_IDS }}
          ECS_SG_ID: ${{ secrets.PROD_ECS_SG_ID }}
        run: |
          TASK_ARN=$(aws ecs run-task \
            --cluster $ECS_CLUSTER \
            --task-definition $MIGRATION_TASK_DEF_ARN \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[$PRIVATE_SUBNET_IDS],securityGroups=[$ECS_SG_ID],assignPublicIp=ENABLED}" \
            --overrides "{
              \"containerOverrides\": [{
                \"name\": \"$CONTAINER_NAME\",
                \"command\": [\"npm\", \"run\", \"db:migrate\"]
              }]
            }" \
            --query 'tasks[0].taskArn' \
            --output text)

          echo "Migration task started: $TASK_ARN"

          aws ecs wait tasks-stopped \
            --cluster $ECS_CLUSTER \
            --tasks $TASK_ARN

          EXIT_CODE=$(aws ecs describe-tasks \
            --cluster $ECS_CLUSTER \
            --tasks $TASK_ARN \
            --query 'tasks[0].containers[0].exitCode' \
            --output text)

          echo "Migration task exit code: $EXIT_CODE"

          if [ "$EXIT_CODE" != "0" ]; then
            echo "Migration failed with exit code $EXIT_CODE"

            echo "===== ECS Task Details ====="
            aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --output json

            echo "===== Container Status ====="
            aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --query 'tasks[0].containers[*].{name:name,lastStatus:lastStatus,exitCode:exitCode,reason:reason}' \
              --output table

            echo "===== Stop Reason ====="
            aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --query 'tasks[0].stoppedReason' \
              --output text
              
            # Derive the log stream from the task ID. ECS awslogs driver writes
            # to: <log-stream-prefix>/<container-name>/<task-id>
            # The logStreamName field on the container is only populated when
            # the task definition's logConfiguration is awslogs — if the field
            # is empty we fall back to deriving it from the task ARN.
            TASK_ID=$(echo "$TASK_ARN" | awk -F'/' '{print $NF}')
            LOG_GROUP="${MIGRATOR_LOG_GROUP:-/ecs/crusource-prod-migrator}"
            LOG_STREAM_DERIVED="ecs/${CONTAINER_NAME}/${TASK_ID}"

            LOG_STREAM_FIELD=$(aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --query 'tasks[0].containers[0].logStreamName' \
              --output text 2>/dev/null || echo "None")

            LOG_STREAM="${LOG_STREAM_FIELD}"
            if [ "$LOG_STREAM" = "None" ] || [ -z "$LOG_STREAM" ]; then
              LOG_STREAM="$LOG_STREAM_DERIVED"
            fi

            echo "===== CloudWatch Log Stream ====="
            echo "Log group:  $LOG_GROUP"
            echo "Log stream: $LOG_STREAM"

            # Brief pause — CloudWatch can lag a few seconds after container exit
            sleep 5

            aws logs get-log-events \
              --log-group-name "$LOG_GROUP" \
              --log-stream-name "$LOG_STREAM" \
              --output text 2>&1 \
              || echo "(CloudWatch logs not found at $LOG_GROUP/$LOG_STREAM — ensure the ECS task execution role has logs:CreateLogGroup and logs:PutLogEvents)"
            exit 1
          fi

          echo "Migration completed successfully"
          
      - name: Download ECS Task Definition
        run: |
          aws ecs describe-task-definition \
          --task-definition $ECS_TASK_DEFINITION \
          --query taskDefinition \
          > task-definition.json

      - name: Render New Task Definition
        id: render
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.event.workflow_run.head_sha }}

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.render.outputs.task-definition }}
          cluster: ${{ env.ECS_CLUSTER }}
          service: ${{ env.ECS_SERVICE }}
          wait-for-service-stability: true
Stage:

name: Deploy Backend to Stage

on:
  workflow_run:
    workflows: ["CI"]
    branches:
      - stage
    types:
      - completed

permissions:
  id-token: write
  contents: read

env:
  AWS_REGION: ${{ secrets.AWS_REGION }}
  ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY }}
  ECS_CLUSTER: ${{ secrets.ECS_CLUSTER }}
  ECS_SERVICE: ${{ secrets.ECS_SERVICE }}
  ECS_TASK_DEFINITION: ${{ secrets.ECS_TASK_DEFINITION }}
  CONTAINER_NAME: ${{ secrets.CONTAINER_NAME }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Checkout Source
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_sha }}

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install Dependencies
        run: npm ci

      - name: Build Application
        run: npm run build

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build Docker Image
        run: |
          docker build \
            --target api \
            -t $ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }} \
            -t $ECR_REPOSITORY:latest \
            .

      - name: Build Migrator Image
        run: |
          docker build \
            --target migrator \
            -t $ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }} \
            .

      - name: Tag Images
        run: |
          docker tag \
          $ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }} \
          ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }}

          docker tag \
          $ECR_REPOSITORY:latest \
          ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:latest

          docker tag \
          $ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }} \
          ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }}

      - name: Push Docker Images
        run: |
          docker push ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:${{ github.event.workflow_run.head_sha }}
          docker push ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:latest
          docker push ${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }}

      - name: Prepare Migration Task Definition
        run: |
          # run-task's containerOverrides does NOT support overriding "image"
          # (only name, command, environment, environmentFiles, cpu, memory,
          # memoryReservation, resourceRequirements are allowed). So we register
          # a dedicated task definition revision that already points at the
          # migrator image, and run that revision instead.
          aws ecs describe-task-definition \
            --task-definition $ECS_TASK_DEFINITION \
            --query taskDefinition \
            > base-task-definition.json

          MIGRATOR_IMAGE="${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:migrator-${{ github.event.workflow_run.head_sha }}"
          LOG_GROUP="/ecs/crusource-stage-migrator"
          REGION="${{ env.AWS_REGION }}"

          # Inject the migrator image AND force a dedicated awslogs logConfiguration
          # so that ALL migrator output is always captured in CloudWatch, regardless
          # of what the base task definition has.
          jq --arg IMAGE "$MIGRATOR_IMAGE" \
             --arg NAME "$CONTAINER_NAME" \
             --arg LOG_GROUP "$LOG_GROUP" \
             --arg REGION "$REGION" '
            .containerDefinitions = (.containerDefinitions | map(
              if .name == $NAME then
                .image = $IMAGE |
                .logConfiguration = {
                  "logDriver": "awslogs",
                  "options": {
                    "awslogs-group": $LOG_GROUP,
                    "awslogs-region": $REGION,
                    "awslogs-stream-prefix": "ecs",
                    "awslogs-create-group": "true"
                  }
                }
              else . end
            )) |
            del(.taskDefinitionArn, .revision, .status, .requiresAttributes,
                .compatibilities, .registeredAt, .registeredBy)
          ' base-task-definition.json > migration-task-definition.json

          echo "=== Migration task definition (container defs) ==="
          jq '.containerDefinitions[] | {name, image, logConfiguration}' migration-task-definition.json

          MIGRATION_TASK_DEF_ARN=$(aws ecs register-task-definition \
            --cli-input-json file://migration-task-definition.json \
            --query 'taskDefinition.taskDefinitionArn' \
            --output text)

          echo "Registered migration task definition: $MIGRATION_TASK_DEF_ARN"
          echo "MIGRATION_TASK_DEF_ARN=$MIGRATION_TASK_DEF_ARN" >> $GITHUB_ENV
          echo "MIGRATOR_LOG_GROUP=$LOG_GROUP" >> $GITHUB_ENV

      - name: Create Migrator Log Group
        run: |
          # AmazonECSTaskExecutionRolePolicy only has CreateLogStream + PutLogEvents,
          # NOT CreateLogGroup. Pre-create from here so the migrator container can
          # write logs immediately without needing awslogs-create-group to work.
          aws logs create-log-group \
            --log-group-name "$MIGRATOR_LOG_GROUP" \
            2>&1 | grep -v "ResourceAlreadyExistsException" || true
          echo "Log group ready: $MIGRATOR_LOG_GROUP"

      - name: Run Database Migrations
        env:
          PRIVATE_SUBNET_IDS: ${{ secrets.PRIVATE_SUBNET_IDS }}
          ECS_SG_ID: ${{ secrets.ECS_SG_ID }}
        run: |
          TASK_ARN=$(aws ecs run-task \
            --cluster $ECS_CLUSTER \
            --task-definition $MIGRATION_TASK_DEF_ARN \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[$PRIVATE_SUBNET_IDS],securityGroups=[$ECS_SG_ID],assignPublicIp=ENABLED}" \
            --overrides "{
              \"containerOverrides\": [{
                \"name\": \"$CONTAINER_NAME\",
                \"command\": [\"npm\", \"run\", \"db:migrate\"]
              }]
            }" \
            --query 'tasks[0].taskArn' \
            --output text)

          echo "Migration task started: $TASK_ARN"

          aws ecs wait tasks-stopped \
            --cluster $ECS_CLUSTER \
            --tasks $TASK_ARN

          EXIT_CODE=$(aws ecs describe-tasks \
            --cluster $ECS_CLUSTER \
            --tasks $TASK_ARN \
            --query 'tasks[0].containers[0].exitCode' \
            --output text)

          echo "Migration task exit code: $EXIT_CODE"

          if [ "$EXIT_CODE" != "0" ]; then
            echo "Migration failed with exit code $EXIT_CODE"

            echo "===== ECS Task Details ====="
            aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --output json

            echo "===== Container Status ====="
            aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --query 'tasks[0].containers[*].{name:name,lastStatus:lastStatus,exitCode:exitCode,reason:reason}' \
              --output table

            echo "===== Stop Reason ====="
            aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --query 'tasks[0].stoppedReason' \
              --output text
              
            # Derive the log stream from the task ID. ECS awslogs driver writes
            # to: <log-stream-prefix>/<container-name>/<task-id>
            # The logStreamName field on the container is only populated when
            # the task definition's logConfiguration is awslogs — if the field
            # is empty we fall back to deriving it from the task ARN.
            TASK_ID=$(echo "$TASK_ARN" | awk -F'/' '{print $NF}')
            LOG_GROUP="${MIGRATOR_LOG_GROUP:-/ecs/crusource-stage-migrator}"
            LOG_STREAM_DERIVED="ecs/${CONTAINER_NAME}/${TASK_ID}"

            LOG_STREAM_FIELD=$(aws ecs describe-tasks \
              --cluster $ECS_CLUSTER \
              --tasks $TASK_ARN \
              --query 'tasks[0].containers[0].logStreamName' \
              --output text 2>/dev/null || echo "None")

            LOG_STREAM="${LOG_STREAM_FIELD}"
            if [ "$LOG_STREAM" = "None" ] || [ -z "$LOG_STREAM" ]; then
              LOG_STREAM="$LOG_STREAM_DERIVED"
            fi

            echo "===== CloudWatch Log Stream ====="
            echo "Log group:  $LOG_GROUP"
            echo "Log stream: $LOG_STREAM"

            # Brief pause — CloudWatch can lag a few seconds after container exit
            sleep 5

            aws logs get-log-events \
              --log-group-name "$LOG_GROUP" \
              --log-stream-name "$LOG_STREAM" \
              --output text 2>&1 \
              || echo "(CloudWatch logs not found at $LOG_GROUP/$LOG_STREAM — ensure the ECS task execution role has logs:CreateLogGroup and logs:PutLogEvents)"
            exit 1
          fi

          echo "Migration completed successfully"
          
      - name: Download ECS Task Definition
        run: |
          aws ecs describe-task-definition \
          --task-definition $ECS_TASK_DEFINITION \
          --query taskDefinition \
          > task-definition.json

      - name: Render New Task Definition
        id: render
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.event.workflow_run.head_sha }}

      - name: Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.render.outputs.task-definition }}
          cluster: ${{ env.ECS_CLUSTER }}
          service: ${{ env.ECS_SERVICE }}
          wait-for-service-stability: true

Frontend:

name: Frontend CI Pipeline

on:
  push:
    branches: [main, stage, dev]
  pull_request:
    branches: [main, stage, dev]

permissions:
  contents: read
  actions: read

jobs:
  validate:
    name: Lint, Test & Build Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Full git history required for Nx affected computation

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Cache Nx
        uses: actions/cache@v4
        with:
          path: .nx/cache
          key: nx-${{ runner.os }}-${{ github.sha }}
          restore-keys: |
            nx-${{ runner.os }}-

      - name: Install dependencies
        run: npm ci

      - name: Set base and head for Nx affected
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            echo "BASE=origin/${{ github.base_ref }}" >> $GITHUB_ENV
            echo "HEAD=HEAD" >> $GITHUB_ENV
          else
            BEFORE_SHA="${{ github.event.before }}"
            if [ -z "$BEFORE_SHA" ] || [ "$BEFORE_SHA" = "0000000000000000000000000000000000000000" ]; then
              echo "BASE=HEAD~1" >> $GITHUB_ENV
            else
              echo "BASE=$BEFORE_SHA" >> $GITHUB_ENV
            fi
            echo "HEAD=HEAD" >> $GITHUB_ENV
          fi

      - name: Check Code Formatting
        run: npx nx format:check --base=$BASE --head=$HEAD

      - name: Run Affected Lint
        run: npx nx affected --target=lint --base=$BASE --head=$HEAD --parallel=3

      - name: Run Affected Tests
        run: npx nx affected --target=test --base=$BASE --head=$HEAD --parallel=3

      - name: Run Affected Builds
        run: npx nx affected --target=build --base=$BASE --head=$HEAD --parallel=3
        env:
          NODE_OPTIONS: '--max-old-space-size=6144'
