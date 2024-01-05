crawl:
	PYTHONPATH=. ./crawlers/crawl.py

build:
	cd web; npm run build

update_recipes:
	cd web; ./update_recipes.py

deploy: update_recipes build
	aws s3 sync --size-only web/build/recipes s3://recipes.oram.ca/recipes --acl public-read
	aws s3 sync --exclude "recipes/*" web/build s3://recipes.oram.ca --acl public-read
	aws cloudfront create-invalidation --distribution-id E3JC9BZDT14T0U --paths "/*"

create_mobile:
	npx react-native init mobile
	mkdir mobile/android/app/src/main/assets
	# add
		# "build:android": "ANDROID_HOME=~/Android/Sdk; react-native build-android --mode=\"release\" --verbose",
		# "release:android": "ANDROID_HOME=~/Android/Sdk; react-native run-android --mode=\"release\"",
		# "android-linux": "react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res && react-native run-android",
	# to scripts in mobile/package.json

mobile_link_assets:
	cd mobile; npx react-native-asset

run_android:
	cd mobile; npm run android-linux

build_android:
	set -e
	cd mobile; npx react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res
	cd mobile; npm run build:android
	cd mobile; npm run release:android

deploy_mobile:
	cp mobile/android/app/build/outputs/apk/release/app-release.apk mobile.apk
	aws s3 cp mobile.apk s3://recipes.oram.ca/mobile.apk --acl public-read
	rm mobile.apk
	aws cloudfront create-invalidation --distribution-id E3JC9BZDT14T0U --paths "/mobile.apk"

bash:
	docker build -t joram87/mobile_builder -f Dockerfile.mobile.builder .
	docker run -v ./mobile:/app -it joram87/mobile_builder bash