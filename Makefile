crawl:
	PYTHONPATH=. ./crawlers/crawl.py

start_mobile_project:
	npx react-native init mobile
	mkdir mobile/android/app/src/main/assets
	# add
		# "build:android": "ANDROID_HOME=~/Android/Sdk; react-native build-android --mode=\"release\" --verbose",
		# "release:android": "ANDROID_HOME=~/Android/Sdk; react-native run-android --mode=\"release\"",
		# "android-linux": "react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res && react-native run-android",
	# to scripts in mobile/package.json

mobile_link_assets:
	nvm use 20; cd mobile; npx react-native-asset

run_android:
	nvm use 20; cd mobile; npm run android-linux

build_android:
	cd mobile; ./update_recipes.py
	nvm use 20; cd mobile; npx react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res
	nvm use 20; cd mobile; npm run build:android
	nvm use 20; cd mobile; npm run release:android

deploy_mobile:
	cp mobile/android/app/build/outputs/apk/release/app-release.apk mobile.apk
	aws s3 cp mobile.apk s3://recipes.oram.ca/mobile.apk --acl public-read
	rm mobile.apk
	aws cloudfront create-invalidation --distribution-id E3JC9BZDT14T0U --paths "/mobile.apk"
