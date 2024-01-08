IMAGE_NAME=joram87/recipe-server

build:
	docker build -t $(IMAGE_NAME) .

run: build
	docker run -p 8000:8000 $(IMAGE_NAME)

deploy:
	aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 431568096872.dkr.ecr.ca-central-1.amazonaws.com
#	aws ecr create-repository --repository-name recipe-server --region ca-central-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
	docker tag $(IMAGE_NAME):latest 431568096872.dkr.ecr.ca-central-1.amazonaws.com/recipe-server:latest
	docker push 431568096872.dkr.ecr.ca-central-1.amazonaws.com/recipe-server:latest

#	aws lambda create-function \
#      --function-name recipes-api \
#      --package-type Image \
#      --region ca-central-1 \
#      --code ImageUri=431568096872.dkr.ecr.ca-central-1.amazonaws.com/recipe-server:latest \
#      --role arn:aws:iam::431568096872:role/recipe-server

	aws lambda update-function-code \
      --function-name recipes-api \
      --region ca-central-1 \
      --image-uri 431568096872.dkr.ecr.ca-central-1.amazonaws.com/recipe-server:latest