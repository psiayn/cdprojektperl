#!/usr/bin/perl
use strict;
use warnings;

print "Hello World!\n";
print 42;

my $animal = "neko";
my $answer = 13;
my @homie = ("chirag","psyian");

print $animal, $answer;
print "lmao","rofl", $animal;

# print $homie[0],$homie[1];

my @animals = ("camel", "llama", "owl");
my @numbers = (23, 12, 123);
my @mixed = ("bruh", 8008,5.5);

# print $animals[0], " ", $animals[1], "\n";

my $i = 0;
until ($i == 5) {
    print $i, "\t";
    $i++;
}

print "\n";

foreach (@animals) {
    print "$_\t";
}

print "\n";

foreach (@numbers) {
    print "$_\t";
}
print "\n";

foreach (@mixed) {
    print "$_\t";
}
print "\n";
