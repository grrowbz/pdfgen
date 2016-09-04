#!/bin/sh
# vim: set ts=4 sw=4 : 

## project top directory
dir=$(cd $(dirname $0)"/.." && pwd)

## application directory
app=$dir/app

## module directory for haru
module_dir=$dir/app/haru

## libharu replace target file
project_file=hpdf.py

cd $dir

## libharuのダウンロード
if [ ! -d ./tmp/libharu ]; then
	git clone https://github.com/libharu/libharu.git ./tmp/libharu
fi

## libharuのビルドに必要なライブラリのインストール
if [ ! `hash yum 2>/dev/null` ]; then
	sudo yum -y install zlib zlib-devel libpng libpng-devel
fi

## libharuのコンパイル
if [ -e ./tmp ]; then
	cd ./tmp/libharu
	./buildconf.sh && ./configure && make 
	sudo make install

	## libharuのライブラリをプロジェクトに配置
	if [ ! -d ${module_dir} ]; then
		mkdir -p ${module_dir}
		cp -rf ./if/python/* ${app}/haru
	fi

	## libharuのファイルにパッチを当てる
	if [ ! -f "${module_dir}/${project_file}.orig" ]; then
		ret=${app}/haru/${project_file}
		realpathcmd='os.path.dirname(os.path.realpath(__file__))+'
		sed -i".orig" -e "s/'libhpdf\.so'/${realpathcmd}'\/lib\/libhpdf\.so'/" ${ret}
	fi
fi

if [ `hash pyenv 2>/dev/null` ]; then
	git clone https://github.com/yyuu/pyenv.git ~/.pyenv

	echo 'export PYENV_ROOT="${HOME}/.pyenv"' >> ~/.bash_profile
	echo 'if [ -n ${PYENV_ROOT} ]; then' >> ~/.bash_profile
	echo '	path=(${PYENV_ROOT}/bin ${PYENV_ROOT}/shims ${path})' >> ~/.bash_profile
	echo 'fi' >> ~/.bash_profile
	echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

	git clone git://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
fi


