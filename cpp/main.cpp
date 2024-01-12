#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <memory>
#include <chrono>


using std_clock = std::chrono::high_resolution_clock;

void test_m(int i){
    auto t0 = std_clock::now();
    auto p = malloc( 1<<i );
    auto t1 = std_clock::now();
    auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
    printf( "m %d, %f, %p\n", i, diff_ns*1e-6, p );
    free(p);
}

void test_c(int i){
    auto t0 = std_clock::now();
    auto p = calloc( 1<<i, 1 );
    auto t1 = std_clock::now();
    auto diff_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1-t0).count();
    printf( "c %d, %f, %p\n", i, diff_ns*1e-6, p );
    free(p);
}

int main(){
    for( int trial=0 ; trial<5 ; ++trial ){
        for( int i=10 ; i<=31 ; ++i ){
            test_m(i);
            test_c(i);
        }
    }
}