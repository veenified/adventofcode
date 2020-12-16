package utils

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"reflect"
	"strconv"
	"strings"
	"time"
	"unicode"
)

// Input returns the input for the specified year and day as a string,
// downloading it if it does not already exist on disk.
func Input(year, day int) string {
	filename := fmt.Sprintf("day%02d_input.txt", day)
	if _, err := os.Stat(filename); err != nil {
		est, err := time.LoadLocation("EST")
		if err != nil {
			panic(err)
		}
		if t := time.Date(year, time.December, day, 0, 0, 0, 0, est); time.Until(t) > 0 {
			fmt.Printf("Puzzle not unlocked yet! Sleeping for %v...\n", time.Until(t))
			time.Sleep(time.Until(t) + 3*time.Second) // don't want to fire too early
		}
		fmt.Println("Downloading input...")
		req, _ := http.NewRequest(http.MethodGet, fmt.Sprintf("https://adventofcode.com/%v/day/%v/input", year, day), nil)
		req.AddCookie(&http.Cookie{
			Name:  "session",
			Value: os.Getenv("AOC_USER_ID"),
		})
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()
		data, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}
		if err := ioutil.WriteFile(filename, data, 0660); err != nil {
			panic(err)
		}
	}
	return ReadInput(filename)
}

// ReadInput returns the contents of filename as a string.
func ReadInput(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return string(bytes.TrimSpace(data))
}

// ExtractInts creates a slice of ints from a string.
func ExtractInts(s string) []int {
	fs := strings.FieldsFunc(s, func(r rune) bool {
		return !unicode.IsDigit(r)
	})
	ints := make([]int, 0, len(fs))
	for _, w := range fs {
		i, err := strconv.Atoi(w)
		if err == nil {
			ints = append(ints, i)
		}
	}
	return ints
}

// Parse parses input into obj based on format.
func Parse(obj interface{}, format string, input string) {
	typ := reflect.TypeOf(obj)
	if typ.Kind() != reflect.Ptr {
		panic("not a pointer!")
	}
	switch typ.Elem().Kind() {
	case reflect.Slice:
		if typ.Elem().Elem().Kind() != reflect.Struct {
			panic("not a pointer to a slice of structs!")
		}
		parseStructSlice(reflect.ValueOf(obj).Elem(), format, input)

	case reflect.Struct:
		parseStruct(reflect.ValueOf(obj).Elem(), format, input)

	default:
		panic("not a pointer to a struct or slice of structs!")
	}
}

// parseStructSlice parse input into slice obj based on format.
func parseStructSlice(obj reflect.Value, format, input string) {
	lines := Lines(input)
	obj.Set(reflect.MakeSlice(obj.Type(), len(lines), len(lines)))
	for i, line := range lines {
		parseStruct(obj.Index(i), format, line)
	}
}

// parseStruct parse input into struct obj based on format.
func parseStruct(obj reflect.Value, format string, input string) {
	var args []interface{}
	for i := 0; i < obj.NumField(); i++ {
		args = append(args, obj.Field(i).Addr().Interface())
	}
	Sscanf(input, format, args...)
}

// Sscanf is a passthrough for fmt.Sscanf that panics upon failure.
func Sscanf(str, format string, args ...interface{}) {
	_, err := fmt.Sscanf(strings.TrimSpace(str), format, args...)
	if err != nil {
		panic(err)
	}
}

// Lines splits a string by newlines.
func Lines(input string) []string {
	return strings.Split(strings.TrimSpace(input), "\n")
}

// Count returns the number of values [x..y) for which fn returns true.
func Count(x int, y int, fn func(i int) bool) (c int) {
	for i := x; i < y; i++ {
		if fn(i) {
			c++
		}
	}
	return
}

// IntToBool returns a bool representation of int i
func IntToBool(i int) bool { return i != 0 }

// BoolToInt returns an int representation of a bool b
func BoolToInt(b bool) int { return map[bool]int{false: 0, true: 1}[b] }

// isNumInRange returns bool if string s is a number and is between ints l and h
func isNumInRange(s string, l, h int) bool {
	n, err := strconv.Atoi(s)
	return err == nil && l <= n && n <= h
}
