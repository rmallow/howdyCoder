python -m pyclean ../
rm -rf data
cd ../data
find . -name '*.txt' | cpio -pdm ../installer/data
find . -name '*.ini' | cpio -pdm ../installer/data
cd ../installer
/usr/local/bin/platypus -B -R -y -i '../howdyCoder/ui/res/MyIcon.icns'  -a 'HowdyCoder'  -o 'None'  -p '/bin/sh'   -I com.rmallow.HowdyCoder -f '../main.py' -f '../requirements.txt' -f '../material.css.template' -f '../howdyCoder' -f 'data' 'start_mac.sh'
codesign -vvv --deep -s "Developer ID Application" -o runtime HowdyCoder.app
ditto -c -k --keepParent HowdyCoder.app HowdyCoder.zip
xcrun notarytool submit HowdyCoder.zip --wait -k ../../../Apple_Connect/AuthKey_CL4R868UJB.p8 -d CL4R868UJB -i 9764afda-07eb-4902-a15a-adafbea5c5bd
xcrun stapler staple HowdyCoder.app
/usr/local/bin/packagesbuild --project HowdyCoder.pkgproj
xcrun notarytool submit installer_output/HowdyCoder.pkg --wait -k ../../../Apple_Connect/AuthKey_CL4R868UJB.p8 -d CL4R868UJB -i 9764afda-07eb-4902-a15a-adafbea5c5bd
xcrun stapler staple installer_output/HowdyCoder.pkg
rm -rf data
