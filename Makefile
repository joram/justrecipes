crawl:
	./crawlers/crawl.py

run_web:
	cd web; yarn start

run_api:
	./api/api.py

build:
	cd api; rm -r build; cd ..
	cd web; yarn build; mv build ../api/build

deploy:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	docker build -t joram87/recipes .
	docker push joram87/recipes