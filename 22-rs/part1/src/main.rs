#![allow(dead_code)]
#![allow(unreachable_code)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_variables)]

use clap::Parser;
use combination::*;
use console::style;
use either::Either;
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressFinish, ProgressStyle};
use num::integer::gcd;
use primal;
use rand::seq::SliceRandom;
use rand::thread_rng;
use rayon::prelude::*;
use std::collections::{HashMap, HashSet};
use std::fs;
use tabled::{
    object::{Rows, Segment},
    Alignment, MaxWidth, Modify, Style, Table, Tabled,
};
static DIRS: [(i32, i32); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

#[derive(Parser, Debug)]
struct Blueprint {
    #[clap(long, default_value_t = 1)]
    id: u32,
    #[clap(short, long, default_value_t = 1)]
    ore_robot_cost: u32,
    #[clap(short, long, default_value_t = 1)]
    clay_robot_cost: u32,
    #[clap(short = 'b', long)]
    obsidian_robot_cost: Vec<u32>,
    #[clap(short, long)]
    geode_robot_cost: Vec<u32>,
}
#[derive(Parser, Debug)]
struct Cli {
    #[clap(short, long, default_value_t = String::from("ex.in"))]
    input_file: String,
}

fn display_grid(grid: &Vec<&str>) {
    grid.iter().for_each(|line| {
        println!("{}", line);
    });
    println!();
}

fn starting_point(grid: &Vec<&str>) -> (usize, usize) {
    let j = grid[0].chars().take_while(|c| *c == ' ').count();

    (0, j)
}

fn next(grid: &Vec<&str>, p: (usize, usize), dir_id: usize) -> (usize, usize) {
    let delta = DIRS[dir_id];
    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    let mut q = (
        (p.0 as i32 + delta.0 + n) % n,
        (p.1 as i32 + delta.1 + m) % m,
    );

    while grid[q.0 as usize].chars().nth(q.1 as usize) == Some(' ') {
        q = ((q.0 + delta.0 + n) % n, (q.1 + delta.1 + m) % m);
    }

    (q.0 as usize, q.1 as usize)
}

fn get_ops(s: &str) -> Vec<Either<char, usize>> {
    let mut ops: Vec<Either<char, usize>> = Vec::new();
    let mut x = 0;
    for c in s.chars() {
        if c == 'L' || c == 'R' {
            if x != 0 {
                ops.push(Either::Right(x));
            }
            ops.push(Either::Left(c));
            x = 0;
        } else {
            x = x * 10 + c.to_digit(10).unwrap() as usize;
        }
    }
    if x != 0 {
        ops.push(Either::Right(x));
    }
    ops
}

fn explore(grid: &Vec<&str>, ops: &Vec<Either<char, usize>>) -> usize {
    let mut p = starting_point(grid);
    let mut dir_id = 0;

    for op in ops {
        if op == &Either::Left('L') {
            dir_id = (dir_id + 4 - 1) % 4;
        }
        if op == &Either::Left('R') {
            dir_id = (dir_id + 1) % 4;
        }

        if let &Either::Right(steps) = op {
            for _ in 0..steps {
                let q = next(grid, p, dir_id);

                if grid[q.0].chars().nth(q.1) == Some('#') {
                    break;
                } else {
                    p = q;
                }
            }
        }
    }
    println!(
        "Arrived at coordinates {}, {}, facing {}",
        p.0 + 1,
        p.1 + 1,
        dir_id
    );

    (p.0 + 1) * 1000 + (p.1 + 1) * 4 + dir_id
}

fn main() {
    let args = Cli::parse();
    // let pb = ProgressBar::new(args.nmax as u64);

    let contents =
        fs::read_to_string(args.input_file).expect("Should have been able to read the file");

    let lines: Vec<&str> = contents.split('\n').collect();
    let lc = lines.len();
    println!("Ops str: {:?}", lines[lines.len() - 2]);
    let ops = get_ops(lines[lines.len() - 2]);
    let grid = lines.into_iter().take(lc - 2).collect();
    display_grid(&grid);
    // println!("Ops: {:?}", ops);

    let s = starting_point(&grid);
    println!("Starting point: {:?}", s);
    assert!(grid[s.0].chars().nth(s.1).unwrap() != ' ');
    assert!(grid[s.0].chars().nth(s.1 - 1).unwrap() == ' ');

    let ans = explore(&grid, &ops);
    println!("Answer is {}", style(ans).red());
}

// 163590 too high
