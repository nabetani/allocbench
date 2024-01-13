package main

import (
	"fmt"
	"os"
	"runtime"
	"time"
)

func test_l(i int) {
	t0 := time.Now()
	defer func() {
		err := recover()
		if err != nil {
			fmt.Printf("l, %v, failed: %v\n", i, err)
		}
	}()
	p := make([]uint8, 1<<i)
	diff := float64(time.Since(t0)) * 1e-6
	fmt.Printf("l, %v, %#v, %p\n", i, diff, &p)
}

func test_c(i int) {
	t0 := time.Now()
	defer func() {
		err := recover()
		if err != nil {
			fmt.Printf("c, %v, failed: %v\n", i, err)
		}
	}()
	p := make([]uint8, 0, 1<<i)
	diff := float64(time.Since(t0)) * 1e-6
	fmt.Printf("c, %v, %#v, %p\n", i, diff, &p)
}

func gc() {
	runtime.GC()
	time.Sleep(time.Second)
}

func main() {
	proc := func() func(int) {
		if 1 < len(os.Args) && os.Args[0] == "c" {
			return test_c
		}
		return test_l
	}()
	for i := 0; i <= 29; i++ {
		proc(i)
		gc()
	}
}
