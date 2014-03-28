for d in `ls|grep -v quick`; do
   cd $d
   mkdir mods
   mv *.* mods
   zip -r $d-1.zip mods
   rm -r mods
   cd ..

done;
