#uniform distribution random
proc udr {min max} {
	set rng [new RNG]
	$rng seed 1
	set r [new RandomVariable/Uniform]
	$r use-rng $rng
	$r set min_ $min
	$r set max_ $max
	return $r

}
proc prr {avg shape} {
	set rng [new RNG]
	$rng seed 1
	set r [new RandomVariable/Pareto]
	$r use-rng $rng
	$r set avg_ $avg
	$r set shape_ $shape
	return $r

}

proc epr {avg} {
	set rng [new RNG]
	$rng seed 1
	set r [new RandomVariable/Exponential]
	$r use-rng $rng
	$r set avg_ $avg
	return $r

}
