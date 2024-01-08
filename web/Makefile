update_recipes:
	./update_recipes.py

deploy: update_recipes
	npm run build
	aws s3 sync --size-only build/recipes s3://recipes.oram.ca/recipes --acl public-read
	aws s3 sync --exclude "recipes/*" build s3://recipes.oram.ca --acl public-read
	aws cloudfront create-invalidation --distribution-id E3JC9BZDT14T0U --paths "/*"
