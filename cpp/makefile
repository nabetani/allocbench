clang.out: main.cpp makefile
	clang++ -std=c++17 -O2 -Wall main.cpp -o clang.out

res_clang: ./clang.out
	./clang.out > res_clang

gcc.out: main.cpp makefile
	g++-13 -std=c++17 -O2 -Wall main.cpp -o gcc.out

res_gcc: ./gcc.out
	./gcc.out > res_gcc