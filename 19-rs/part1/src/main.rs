use clap::Parser;
use console::style;
use std::collections::HashMap;

fn explore(
    args: &Cli,
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
            println!("Found new best: {} (score = {})", g, g * bp.id);
            *best = g;
        }
        return g;
    }

    let mut ret = 0;

    let gc = &bp.geode_robot_cost;
    let bc = &bp.obsidian_robot_cost;
    let cc = &bp.clay_robot_cost;
    let oc = &bp.ore_robot_cost;

    if o >= gc[0] && b >= gc[1] {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                bp,
                best,
                (or, cr, br, gr + 1),
                (o + or - gc[0], c + cr, b + br - gc[1], g + gr),
                t + 1,
            ),
        );
    }
    if t + 1 < args.tmax && o >= bc[0] && c >= bc[1] {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                bp,
                best,
                (or, cr, br + 1, gr),
                (o + or - bc[0], c + cr - bc[1], b + br, g + gr),
                t + 1,
            ),
        );
    }
    if t + 1 < args.tmax && o >= *cc {
        ret = std::cmp::max(
            ret,
            explore(
                args,
                bp,
                best,
                (or, cr + 1, br, gr),
                (o + or - cc, c + cr, b + br, g + gr),
                t + 1,
            ),
        );
    }
    if t + 1 < args.tmax && o >= *oc {
        ret = std::cmp::max(
            ret,
            explore(
                args,
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
    #[clap(short, long, default_value_t = 24)]
    tmax: u32,
}

fn main() {
    let args = Cli::parse();

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
        (
            4,
            Blueprint {
                id: 4,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 18],
                geode_robot_cost: vec![2, 11],
            },
        ),
        (
            5,
            Blueprint {
                id: 5,
                ore_robot_cost: 4,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![4, 16],
                geode_robot_cost: vec![2, 15],
            },
        ),
        (
            6,
            Blueprint {
                id: 6,
                ore_robot_cost: 2,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 11],
                geode_robot_cost: vec![3, 14],
            },
        ),
        (
            7,
            Blueprint {
                id: 7,
                ore_robot_cost: 2,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 17],
                geode_robot_cost: vec![3, 11],
            },
        ),
        (
            8,
            Blueprint {
                id: 8,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![2, 14],
                geode_robot_cost: vec![4, 19],
            },
        ),
        (
            9,
            Blueprint {
                id: 9,
                ore_robot_cost: 2,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 18],
                geode_robot_cost: vec![2, 19],
            },
        ),
        (
            10,
            Blueprint {
                id: 10,
                ore_robot_cost: 3,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 19],
                geode_robot_cost: vec![3, 17],
            },
        ),
        (
            11,
            Blueprint {
                id: 11,
                ore_robot_cost: 2,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 11],
                geode_robot_cost: vec![3, 8],
            },
        ),
        (
            12,
            Blueprint {
                id: 12,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 17],
                geode_robot_cost: vec![2, 13],
            },
        ),
        (
            13,
            Blueprint {
                id: 13,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![2, 15],
                geode_robot_cost: vec![2, 13],
            },
        ),
        (
            14,
            Blueprint {
                id: 14,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![3, 18],
                geode_robot_cost: vec![4, 16],
            },
        ),
        (
            15,
            Blueprint {
                id: 15,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 5],
                geode_robot_cost: vec![3, 15],
            },
        ),
        (
            16,
            Blueprint {
                id: 16,
                ore_robot_cost: 2,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 13],
                geode_robot_cost: vec![2, 20],
            },
        ),
        (
            17,
            Blueprint {
                id: 17,
                ore_robot_cost: 3,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![2, 7],
                geode_robot_cost: vec![2, 9],
            },
        ),
        (
            18,
            Blueprint {
                id: 18,
                ore_robot_cost: 4,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![4, 15],
                geode_robot_cost: vec![3, 12],
            },
        ),
        (
            19,
            Blueprint {
                id: 19,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 18],
                geode_robot_cost: vec![3, 8],
            },
        ),
        (
            20,
            Blueprint {
                id: 20,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![2, 7],
                geode_robot_cost: vec![4, 13],
            },
        ),
        (
            21,
            Blueprint {
                id: 21,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 5],
                geode_robot_cost: vec![4, 8],
            },
        ),
        (
            22,
            Blueprint {
                id: 22,
                ore_robot_cost: 2,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![2, 14],
                geode_robot_cost: vec![3, 8],
            },
        ),
        (
            23,
            Blueprint {
                id: 23,
                ore_robot_cost: 2,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![2, 15],
                geode_robot_cost: vec![3, 16],
            },
        ),
        (
            24,
            Blueprint {
                id: 24,
                ore_robot_cost: 3,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 18],
                geode_robot_cost: vec![3, 13],
            },
        ),
        (
            25,
            Blueprint {
                id: 25,
                ore_robot_cost: 2,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 15],
                geode_robot_cost: vec![2, 20],
            },
        ),
        (
            26,
            Blueprint {
                id: 26,
                ore_robot_cost: 2,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![3, 17],
                geode_robot_cost: vec![4, 20],
            },
        ),
        (
            27,
            Blueprint {
                id: 27,
                ore_robot_cost: 3,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 17],
                geode_robot_cost: vec![2, 13],
            },
        ),
        (
            28,
            Blueprint {
                id: 28,
                ore_robot_cost: 3,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![3, 15],
                geode_robot_cost: vec![2, 8],
            },
        ),
        (
            29,
            Blueprint {
                id: 29,
                ore_robot_cost: 4,
                clay_robot_cost: 3,
                obsidian_robot_cost: vec![4, 19],
                geode_robot_cost: vec![4, 12],
            },
        ),
        (
            30,
            Blueprint {
                id: 30,
                ore_robot_cost: 4,
                clay_robot_cost: 4,
                obsidian_robot_cost: vec![4, 14],
                geode_robot_cost: vec![2, 16],
            },
        ),
    ]);

    let blueprint = tests.get(&args.blueprint).expect("Blueprint not found");

    let mut best = 0;
    let ans = explore(&args, blueprint, &mut best, (1, 0, 0, 0), (0, 0, 0, 0), 0);
    println!(
        "Answer for blueprint {} is {} (score = {})",
        blueprint.id,
        ans,
        style(ans * blueprint.id).red()
    );
}
