sphinx-build -b htmlhelp doc doctmp
"C:\Program Files\HTML Help Workshop\hhc.exe" doctmp\formlayout.hhp
"C:\Program Files (x86)\HTML Help Workshop\hhc.exe" doctmp\formlayout.hhp
copy doctmp\formlayout.chm .
7z a formlayout.chm.zip formlayout.chm
del doctmp\formlayout.chm
del doc.zip
sphinx-build -b html doc doctmp
cd doctmp
7z a -r ..\doc.zip *.*
cd ..
rmdir /S /Q doctmp
del formlayout.chm.zip
