use strict;
use warnings;
print "Hello World!\n";
print 42;
my $iter = 3;
my $animal = "neko";
my $answer = 13;
my @homie = ("chirag","psyian");
my @newarr = (1,2,3,4,5);
print $animal, $answer;
print "lmao","rofl", $animal;
print $homie[0],$homie[1];
my @animals = ("camel", "llama", "owl");
my @numbers = (23, 12, 123);
my @mixed = ("bruh", 8008,5.5);
print $animals[0], " ", $animals[1], "\n";
my $i = 0;
until ($i == 5) {
    print $i, "\t";
    print $animals[$i];
    $i++;
}
print "\n";
foreach (@animals) {
    print "$_\t";
}
print "\n";
until ($newarr[0] == 3)
{
    print $iter;
    my $hello_there;
    $newarr[0]++;
}
foreach (@numbers) {
    print "$_\t";
}
print "\n";
foreach (@mixed) {
    print "$_\t";
}
print "\n";

# jprinta
#ilasjdfljasf
# print $test;
# my $test;
