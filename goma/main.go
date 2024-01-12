package main

import (
	"fmt"
	"time"
)

func test(i int) {
	t0 := time.Now()
	p := make([]uint8, 1<<i)
	diff := float64(time.Since(t0)) * 1e-6
	fmt.Printf("%v, %#v, %p\n", i, diff, &p)
}

func main() {
	for trial := 0; trial < 5; trial++ {
		for i := 10; i <= 31; i++ {
			test(i)
		}
	}
}
