# KLAN 2016

Nástroje pro reverzní inženýring původních CD-ROM časopisu KLAN. Cílem je získat pro každou instanci všech binárních knihoven strukturovaná JSON metadata a zdrojové bloby. Na základě těchto podkladů je následně možné vytvářet pro jednotlivé knihovny (texty, fonty, obrázky, hudba, audia, videa atd.) zjednodušená JSON schémata a multimediální soubory v obecně standardizovaných formátech (HTML, GIF, PNG, MOD, WAV, AVI atd.).

## Python

https://www.python.org

Instalace:

```bash
sudo apt-get install python libarchive-dev
TODO venv
```

## Kaitai Struct

http://kaitai.io  
https://github.com/kaitai-io/kaitai_struct  
http://doc.kaitai.io/user_guide.html  
http://doc.kaitai.io/ksy_reference.html

### Kaitai Struct: compiler (ksc)

https://github.com/kaitai-io/kaitai_struct_compiler  
http://doc.kaitai.io/developers.html

Instalace aktuální verze ze zdrojových kódů (jako DEB balíček pro Debian/*buntu):

```bash
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get update
sudo apt-get install git dpkg-dev dpkg-sig fakeroot lintian sbt default-jre-headless
git clone https://github.com/kaitai-io/kaitai_struct_compiler.git
cd kaitai_struct_compiler
sbt compilerJVM/debian:packageBin
cd jvm/target
sudo dpkg -i *.deb
```

There is an official .deb repository available for Debian and Ubuntu-based distributions. Just add it and install a package:

```bash
sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net --recv 379CE192D401AB61
echo "deb https://dl.bintray.com/kaitai-io/debian_unstable jessie main" | sudo tee /etc/apt/sources.list.d/kaitai.list
sudo apt-get update
sudo apt-get install kaitai-struct-compiler
```

### Kaitai Struct: visualizer (ksv)

https://github.com/kaitai-io/kaitai_struct_visualizer

Instalace aktuální verze ze zdrojových kódů (jako Ruby gem):

```bash
sudo apt-get install git ruby
git clone https://github.com/kaitai-io/kaitai_struct_visualizer.git
cd kaitai_struct_visualizer
gem build kaitai-struct-visualizer.gemspec
sudo gem install kaitai-struct-visualizer-0.7.gem
```

### Kaitai Struct: runtime library for Python

https://github.com/kaitai-io/kaitai_struct_python_runtime  
https://pypi.python.org/pypi/kaitaistruct  
http://doc.kaitai.io/lang_python.html

Instalace aktuální verze ze zdrojových kódů (jako Python modul):  
TODO in venv!

```bash
sudo apt-get install git python3 python-enum34 python3-setuptools
git clone https://github.com/kaitai-io/kaitai_struct_python_runtime.git
cd kaitai_struct_python_runtime
sudo python3 setup.py install
```

## Pomocné nástroje

### 010 Editor

https://www.sweetscape.com/010editor/

### DOSBox

https://www.dosbox.com

### IDA

https://www.hex-rays.com/products/ida/

### IDA / DOSBox debugger

https://github.com/wjp/idados  
https://github.com/wjp/dosbox  
https://github.com/wjp/idados/issues/7  
https://github.com/wjp/idados/issues/10  
https://www.dosbox.com/wiki/Building_DOSBox_with_MinGW

### Retargetable Decompiler (RetDec)

https://retdec.com
