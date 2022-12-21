#![allow(dead_code)]
#![allow(unreachable_code)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_variables)]

use clap::Parser;
use combination::*;
use console::style;
use indicatif::{ParallelProgressIterator, ProgressBar, ProgressFinish, ProgressStyle};
use num::integer::gcd;
use primal;
use rand::rngs::ThreadRng;
use rand::seq::SliceRandom;
use rand::thread_rng;
use rand::Rng;
use rayon::prelude::*;
use std::collections::{HashMap, HashSet};
use tabled::{
    object::{Rows, Segment},
    Alignment, MaxWidth, Modify, Style, Table, Tabled,
};
static mut BEST: u32 = 0;

fn explore(
    args: &Cli,
    rng: &mut ThreadRng,
    bp: &Blueprint,
    best: &mut u32,
    robots: (u32, u32, u32, u32),
    resources: (u32, u32, u32, u32),
    t: u32,
) -> u32 {
    let (or, cr, br, gr) = robots;
    let (o, c, b, g) = resources;
    if t == args.tmax {
        if &g > best {
            println!("Found new best: {}", g);
            *best = g;
        }
        return g;
    }

    let mut ret = 0;

    let gc = &bp.geode_robot_cost;
    let bc = &bp.obsidian_robot_cost;
    let cc = &bp.clay_robot_cost;
    let oc = &bp.ore_robot_cost;

    if o >= gc[0] && b >= gc[1] && &rng.gen::<f32>() <= &args.pg {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                rng,
                bp,
                best,
                (or, cr, br, gr + 1),
                (o + or - gc[0], c + cr, b + br - gc[1], g + gr),
                t + 1,
            ),
        );
    }
    if t + 1 < args.tmax && o >= bc[0] && c >= bc[1]  && &rng.gen::<f32>() <= &args.pb {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                rng,
                bp,
                best,
                (or, cr, br + 1, gr),
                (o + or - bc[0], c + cr - bc[1], b + br, g + gr),
                t + 1,
            ),
        );
    }
    if t + 1 < args.tmax && o >= *cc  && &rng.gen::<f32>() <= &args.pc {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                rng,
                bp,
                best,
                (or, cr + 1, br, gr),
                (o + or - cc, c + cr, b + br, g + gr),
                t + 1,
            ),
        );
    }
    if t + 1 < args.tmax && o >= *oc  && &rng.gen::<f32>() <= &args.po {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                rng,
                bp,
                best,
                (or + 1, cr, br, gr),
                (o + or - oc, c + cr, b + br, g + gr),
                t + 1,
            ),
        );
    }
    ret = std::cmp::max(
        ret,
        explore(
            args,
            rng,
            bp,
            best,
            (or, cr, br, gr),
            (o + or, c + cr, b + br, g + gr),
            t + 1,
        ),
    );
    ret
}

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
    #[clap(short, long, default_value_t = 1)]
    blueprint: u32,
    #[clap(short, long, default_value_t = 32)]
    tmax: u32,
    #[clap(long, default_value_t = 1.0)]
    po: f32,
    #[clap(long, default_value_t = 1.0)]
    pc: f32,
    #[clap(long, default_value_t = 1.0)]
    pb: f32,
    #[clap(long, default_value_t = 1.0)]
    pg: f32,
}

fn main() {
    let args = Cli::parse();
    // let pb = ProgressBar::new(args.nmax as u64);

    let tests = HashMap::from([
        (
            1,
            Blueprint {
                id: 1,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 13],
                geode_robot_cost: vec![3, 7],
            },
        ),
        (
            2,
            Blueprint {
                id: 2,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 20],
                geode_robot_cost: vec![2, 12],
            },
        ),
        (
            3,
            Blueprint {
                id: 3,
                ore_robot_cost: 3,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 9],
                geode_robot_cost: vec![3, 7],
            },
        ),
    ]);

    let blueprint = tests.get(&args.blueprint).expect("Blueprint not found");

    let mut rng = rand::thread_rng();

    let mut best = 0;
    let ans = explore(
        &args,
        &mut rng,
        &blueprint,
        &mut best,
        (1, 0, 0, 0),
        (0, 0, 0, 0),
        0,
    );
    println!(
        "Answer for blueprint {} is {}",
        blueprint.id,
        style(ans).red()
    );
}
