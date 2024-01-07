IMAGE_NAME=joram87/recipe-server

build:
	docker build -t $(IMAGE_NAME) .

run: build
	docker run -p 8000:8000 $(IMAGE_NAME)

deploy: build
	docker push $(IMAGE_NAME)
	ssh john@192.168.1.222 "cd ~/projects/nas; docker compose pull recipes; docker compose up -d recipes"