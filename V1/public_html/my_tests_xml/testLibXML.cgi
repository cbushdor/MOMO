#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
my $FichierXML = 'ExempleXML.xml';
my $parser     = XML::LibXML->new();
# Activation validation DTD du fichier XML avant le parsing
$parser->validation(1);
my $tree = $parser->parse_file($FichierXML);
# Création du fichier résultat
my $FichierResulat = 'resultat.txt';
open( my $FhResultat, '>', $FichierResulat )
  or die("Impossible d'ouvrir le fichier $FichierResulat\n$!");
# Racine du document XML
my $root = $tree->getDocumentElement;
# Validation XSD du fichier XML
# Récupérons le fichier XSD dans la balise annuaire
my $FichierXSD = $root->getAttribute('xsi:noNamespaceSchemaLocation');
my $schema = XML::LibXML::Schema->new( location => $FichierXSD );
eval { $schema->validate($tree) };
die "[XSD] Le fichier $FichierXML est non valide.\n$@" if $@;
# Balise personne
my @personne = $root->getElementsByTagName('personne');
foreach my $childid (@personne) {
  print {$FhResultat} "Personne : ",
    $childid->getElementsByTagName('prenom')->[0]->getFirstChild->getData, " ",
    $childid->getAttribute('miseajour'), "\n";
  print {$FhResultat} "Role : ",
    $childid->getElementsByTagName('role')->[0]->getFirstChild->getData, "\n";
  print {$FhResultat} "Email : ",
    $childid->getElementsByTagName('email')->[0]->getFirstChild->getData, "\n";
  foreach my $telephone ( $childid->getElementsByTagName('telephone') ) {
    print {$FhResultat} "Telephone : ", $telephone->getFirstChild->getData,
      "\n";
  }
  foreach my $langage ( $childid->getElementsByTagName('langage') ) {
    print {$FhResultat} "Langage prefere : ", $langage->getAttribute('name'),
      "\n";
  }
  foreach my $modules ( $childid->getElementsByTagName('ModulePreferes') ) {
    print {$FhResultat} "\t- ", $modules->getFirstChild->getData, "\n";
  }
  # commentaire
  print {$FhResultat} "Commentaire : ",
    $childid->getElementsByTagName('commentaire')->[0]->getFirstChild->getData,
    "\n";
  print {$FhResultat} "\n", "=" x 10, "\n\n";
}
close($FhResultat);
