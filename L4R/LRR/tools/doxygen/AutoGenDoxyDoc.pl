my $daten;
my $daten1;

print "Begin\n";

open (DATEI, "Doxyfile_Template");
   while(<DATEI>){
     $daten1 = $daten1.$_;
   }
close (DATEI);

open (DATEI, "DoxyfileVar");
   while(<DATEI>){
     $daten = $daten.$_;
   }
close (DATEI);

open (DATEI, ">Doxyfile");
   print DATEI $daten1, $daten;
close (DATEI);

print `"C:/Program Files/doxygen/bin/doxygen.exe" Doxyfile`;

print "Start Doku HTML\n";
  
print "End\n";

#<STDIN>
