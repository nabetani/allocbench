#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <memory>
#include <chrono>
#include <map>
#include <vector>
#include <string>

using std_clock = std::chrono::high_resolution_clock;
using namespace std::literals::string_literals;

void test_m(int i){
    auto t0 = std_clock::now();
    auto p = malloc( size_t(i)<<i );
    auto t1 = std_clock::now();
    auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
    printf( "m, %d, %f, %p\n", i, diff_ns*1e-6, p );
    free(p);
}

void test_c(int i){
    auto t0 = std_clock::now();
    auto p = calloc( size_t(i)<<i, 1 );
    auto t1 = std_clock::now();
    auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
    printf( "c, %d, %f, %p\n", i, diff_ns*1e-6, p );
    free(p);
}

void test_v(int i){
    auto t0 = std_clock::now();
    try{
        auto p = std::vector<char>(size_t(i)<<i);
        auto t1 = std_clock::now();
        auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
        printf( "v, %d, %f, %p\n", i, diff_ns*1e-6, p.data() );
    }
    catch( std::exception & e ){
        printf( "v, %d, fail\n", i);
    }
}

void test_r(int i){
    auto t0 = std_clock::now();
    try{
        auto p = std::vector<char>();
        p.reserve(size_t(i)<<i);
        auto t1 = std_clock::now();
        auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
        printf( "v, %d, %f, %p\n", i, diff_ns*1e-6, p.data() );
    }
    catch( std::exception & e ){
        printf( "v, %d, fail\n", i);
    }
}

void test_s(int i){
    auto t0 = std_clock::now();
    try{
        auto p = std::vector<char>();
        p.resize(size_t(i)<<i);
        auto t1 = std_clock::now();
        auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
        printf( "v, %d, %f, %p\n", i, diff_ns*1e-6, p.data() );
    }
    catch( std::exception & e ){
        printf( "v, %d, fail\n", i);
    }
}

void test_n(int i){
    auto t0 = std_clock::now();
    try{
        auto p = new char[size_t(i)<<i];
        auto t1 = std_clock::now();
        auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
        printf( "v, %d, %f, %p\n", i, diff_ns*1e-6, p);
    }
    catch( std::exception & e ){
        printf( "v, %d, fail\n", i);
    }
}

int main(int argc, char const * argv[]){
    typedef void (*tester_t)(int);
    tester_t test = std::map<std::string,tester_t>({
        { "c"s, test_c },
        { "m"s, test_m },
        { "v"s, test_v },
        { "r"s, test_r },
        { "s"s, test_s },
        { "n"s, test_n },
    })[argv[1]];
    for( int i=1 ; i<=29 ; ++i ){
        test(i);
    }
}