#!/usr/bin/env python

# Small change to add to commit.
import tkinter
from sopel.modules import *
tclsh = tkinter.Tcl()

@sopel.module.commands('.{category}')
def category(bot, trigger):
    tclsh.eval("""
set quotedir "/usr/lib/eggdrop/scripts/categories/"
set quotevianotice 0

bind pubm - "% \\\?*" quote:pub:quote
bind pubm - "% \\\!*" quote:pub:quote
bind pubm - "% \\\!add*" quote:pub:addquote
bind msgm - "% \\\?*" quote:msgm:quote


proc quote:msgm:quote {nick uhost hand chan arg} {
        regsub -all {[?!]([a-zA-Z0-9]+).*$} $arg "\\1" category
        regsub -all {[?!][a-zA-Z0-9]+(\s*)(.*)?$} $arg {\2} pattern

        if { $category == "?" || $nick == "Athene" } {
                return 1
        }
        set quote [getquote $category $pattern]
        if { $quote == "" } {
                putserv "NOTICE $nick :No matching quote in category $category"
        } else {
                putserv "NOTICE $nick :$quote"
        }
}

proc quote:pub:quote {nick uhost hand chan arg} {
        regsub -all {[!?](add)?([a-zA-Z0-9]+).*$} $arg {\1} add
        regsub -all {[!?](add)?([a-zA-Z0-9]+).*$} $arg {\2} category
        regsub -all {[!?][a-zA-Z0-9]+(\s*)(.*)?$} $arg {\2} pattern


        if { $category == "?" || $nick == "Athene" } {
                return 1
        }
        if { $add == "add" } {
                global quotedir
                set quotefile "$quotedir/$category.txt"

                if { $quote == "" } {
                        putserv "PRIVMSG $chan :Usage: !add<category> <a quote>"
                        return 0
                }

                set file [open $quotefile a]
                puts $file $quote
                close $file
                return 1
        } elseif { $category == "taunt" || $category == "scrap" || $category == "w" || $category == "fml" || $category == "8ball" || $category == "roll" || $category == "gpatent" || $category == "gbook" || $category == "glocal" || $category == "gnews" || $category == "gvideo" || $category == "google" || $category == "gimage"} {
                return 1
        } else {
                if { $category == "random" } {
                        global quotedir
                        set filelist [ glob -directory $quotedir -- *.txt  ]
                        set row [ rand [llength $filelist] ]
                        set file [ lindex $filelist $row ]
                        set category [ string range $file 19 end-4]
                        set command "!$category"
                        set quote [getquote $nick $uhost $hand $chan $command ]
                        putserv "PRIVMSG $chan :From $category > $quote"
                } else {
                        set quote [getquote $nick $uhost $hand $chan $arg ]
                        if { $quote == "" } {
                                putserv "PRIVMSG $chan :No matching quote in category $category"
                        } else {
                                putserv "PRIVMSG $chan :$quote"
                        }
                }
        }
}

proc quote:pub:addquote {nick uhost hand chan arg} {
        regsub -all {\!add([a-zA-Z0-9]+).*$} $arg "\\1" category
        regsub -all {\!add[a-zA-Z0-9]+(\s*)(.*)?$} $arg {\2} quote
        global quotedir
        set quotefile "$quotedir/$category.txt"

        if { $quote == "" } {
                putserv "PRIVMSG $chan :Usage: !add<category> <a quote>"
                return 0
        }

        set file [open $quotefile a]
        puts $file $quote
        close $file
        return 1
}

proc getquote {nick uhost hand chan command} {
        regsub -all {[!?](add)?([a-zA-Z0-9]+).*$} $command {\1} add
        regsub -all {[!?](add)?([a-zA-Z0-9]+).*$} $command {\2} category
        regsub -all {[!?][a-zA-Z0-9]+(\s*)(.*)?$} $command {\2} arg
        global quotedir
        set quotefile "$quotedir/$category.txt"
        set quotescript "$quotedir/$category.tcl"
        set quotes ""
        if { [file exists $quotescript] } {
                putlog "executing $quotescript"
                source $quotescript
                run_command $nick $uhost $hand $chan $arg
        } elseif { [file exists $quotefile] } {
                putlog "opening $quotefile"
                set file [open "$quotefile" r]
        } else {
                return "";
        }
        while { ![eof $file] } {
                set quote [gets $file]
                if { $quote != "" } {
                        set quotes [linsert $quotes end $quote]
                }
        }
        close $file
        if { $arg != "" } {
                set pattern [string tolower $arg]
                set aquotes ""
                set quote ""
                foreach quote $quotes {
                        set lowquote [string tolower $quote]
                        if { [string match $pattern $lowquote] } {
                                set aquotes [linsert $aquotes end $quote]
                        }
                        set quotes ""
                        set quotes $aquotes
                }
        }
        set row [rand [llength $quotes]]
        if { [expr $row >= 0] && [expr $row < [llength $quotes]] } {
                set quote [lindex $quotes $row]
        }

        return $quote
};
""")
