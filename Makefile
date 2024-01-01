crawl:
	./crawlers/crawl.py

run_web:
	cd web; yarn start

run_api:
	./api/api.py

build:
	cd web; npm run build

update_recipes:
	cd web; ./update_recipes.py

#deploy: update_recipes build
deploy:
	aws s3 sync --size-only web/build/recipes s3://recipes.oram.ca/recipes --acl public-read
	aws s3 sync --exclude "recipes/*" web/build s3://recipes.oram.ca --acl public-read
	aws cloudfront create-invalidation --distribution-id E3JC9BZDT14T0U --paths "/index.html" "/static/*"