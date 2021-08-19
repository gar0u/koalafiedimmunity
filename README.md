# koalafiedimmunity
Simple fix to protect files from ransomware

Most ransomware only encrypts the first 256K or 1MB of a file.

KoalafiedImmunity copys the first 1MB of a file and appends it to the end of the file.  This does not break the functionality of most file types.  Microsoft Office file types (doxc, xlxs, pptx, etc.) will appear corrupted, but their associated applications can recover them.

Files smaller than 1MB are padded with null bytes (0x00) first.

This is currently just a proof-of-concept.  Of course new ransomware could evolve to combat this mitigation.  This simple tool asymetrically changes the costs of ransomware.  Files are immune to old ransomware without the need of backups.  New ransomware must encrypt a larger portion of each file, slowing down the attack and giving more time to defenders to detect and mitigate the attack.

There is a lot of technical debt in this proof of concept, including:
    1. The code is unpythonic
    2. The directory to operate on is hard coded and should come from sys.argv
    3. Subsequent runs continue to append the first 1MB to the end of the file.
    4. There is no restore function (yet)
