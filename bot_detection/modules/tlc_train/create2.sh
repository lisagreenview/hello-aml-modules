PATH=mingw/bin:.:$PATH
INFILE1=$1
shift
OUTTLC1=$1
shift
OUTSTAT1=$1
shift
INFILE2=$1
shift
OUTTLC2=$1
shift
OUTSTAT2=$1
shift
NORM=$1

REST=$*

if [ "$NORM" == "/norm+" ]; then
  TLCEXT=norm.tlc
  STATEXT=norm.stat.tsv
else
  TLCEXT=tlc
  STATEXT=stat.tsv
fi

# We could run on the original input file and move the resulting .tlc file to the output dir
# but, after some consultation with the Aether team, they recommend against this because
# it's possible that in the future the input will become a readonly hard link, so it's better
# if I write to "." instead. So, even though it's technically a bit slower, I'll copy the input
# to the local dir, run, then copy the output to the output dir.
# Also, just in case it crosses drives, I'm going to copy instead of "move" the .tlc file to the output
#
# For filename, generates filename.tlc and filename.stat.tsv
# except if /norm, then generates filename.norm.tlc and filename.norm.stat.tsv

# copy is a DOS command, xcopy prompts for dir vs. file, robocopy needs dirs, cp needs / instead of \, so...
echo Copying Aether input files to local 
cmd /c "copy $INFILE1 localinfile1"
cmd /c "copy $INFILE2 localinfile2"
cmd /c "TL.exe /c CreateInstances localinfile1 /test localinfile2 $REST"
echo Copying output files to Aether output
cmd /c "copy localinfile1.$TLCEXT $OUTTLC1"
cmd /c "copy localinfile1.$STATEXT $OUTSTAT1"
cmd /c "copy localinfile2.$TLCEXT $OUTTLC2"
cmd /c "copy localinfile2.$STATEXT $OUTSTAT2"

