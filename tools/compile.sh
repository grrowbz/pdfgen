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
	/bin/sudo yum -y install zlib zlib-devel libpng libpng-devel
fi

## libharuのコンパイル
if [ -e ./tmp ]; then
	cd ./tmp/libharu
	./buildconf.sh && ./configure --prefix=${module_dir} && make && make install
	## libharuのライブラリをプロジェクトに配置
	cp -rf ./if/python/* ${app}/haru

	## libharuのファイルにパッチを当てる
	if [ ! -f "${module_dir}/${project_file}.orig" ]; then
		ret=${app}/haru/${project_file}
		realpathcmd='os.path.dirname(os.path.realpath(__file__))+'
		sed -i".orig" -e "s/'libhpdf\.so'/${realpathcmd}'\/lib\/libhpdf\.so'/" ${ret}
	fi
fi

