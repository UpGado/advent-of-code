using IterTools
using ProgressBars


function read_moons(filename)
    exp = r"<x=([+-]?\d+), y=([+-]?\d+), z=([+-]?\d+)"
    pos = [map(x -> parse(Int, x), match(exp, ln).captures)
            for ln in eachline(open(filename))]
    pos = hcat(pos...)
    vel = zeros(Int, size(pos))
    moons = cat(pos, vel, dims=3)
    return moons
end

function simulate_gravity!(moons_col)
    for (m1, m2) in subsets(moons_col, 2)
        m1p, m2p = map(m -> view(m, :, 1), [m1, m2])
        m1v, m2v = map(m -> view(m, :, 2), [m1, m2])
        for dim in 1:3
            if m1p[dim] != m2p[dim]
                delta = if (m1p[dim] > m2p[dim]) 1 else -1 end
                m1v[dim] -= delta
                m2v[dim] += delta
            end
        end
    end
end

function simulate_velocity!(moons)
    vel = view(moons, :, :, 2)
    pos = view(moons, :, :, 1)
    moons[:, :, 1] = pos + vel
end

function simulate_step!(moons)
    moons_col = [c for c in eachslice(moons, dims=2)]
    simulate_gravity!(moons_col)
    simulate_velocity!(moons)
end


moons = read_moons("input.txt")

# part 1

function simulate(moons; t_steps=10, call_each_step=nothing)
    moons = copy(moons)
    for t in ProgressBar(1:t_steps)
        simulate_step!(moons)
    end
    return moons
end

function total_energy(moons)
    abs_vals = abs.(moons)
    energy = sum(abs_vals, dims=1)
    total_energy = energy[:, :, 1].*energy[:, :, 2]
    return sum(total_energy)
end


_moons = simulate(moons, t_steps=1000)
@show total_energy(_moons)

# part 2

function detect_cycles_dim(moons, dim)
    moons = copy(moons)
    states = Set()
    for t in Iterators.countfrom(0)
        simulate_step!(moons)
        dim_state = tuple(moons[dim, :, :]...)
        if dim_state in states
            return t
        else
            push!(states, dim_state)
        end
    end
end

function detect_cycle(moons)
    dim_cycles = [detect_cycles_dim(moons, dim) for dim in 1:3]
    return lcm(dim_cycles)
end

@show detect_cycle(moons)
