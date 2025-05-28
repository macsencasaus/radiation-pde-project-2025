import { useState, useEffect, useRef } from "react";
// const Desmos = require("desmos")
// import * as Desmos from "desmos";

// type NumberType = "Int" | "Float";
// interface Field<T> {
//     name: string;
//     fieldType: NumberType;
//     setFieldArr: React.Dispatch<React.SetStateAction<T>>;
// }

function App() {
    const defaultTol = 0.0001;
    const defaultMaxIter = 1000;

    const defaultNZones = 5;
    const defaultCells = [25, 25, 25, 25, 25];
    const defaultZoneLength = [2, 1, 2, 1, 2];
    const defaultSigmaS = [0, 0, 0, 0.9, 0.9];
    const defaultSigmaT = [50, 5, 0, 1, 1];
    const defaultSource = [25, 0, 0, 0.5, 0];
    const defaultBoundaryValues = [0, 0];
    const defaultSUPGTuningValue = 1;

    const [tol, setTol] = useState<number>(defaultTol);
    const [maxIter, setMaxIter] = useState<number>(defaultMaxIter);

    const [nZones, setNZones] = useState<number>(defaultNZones);
    const [cells, setCells] = useState<number[]>(defaultCells);
    const [zoneLength, setZoneLength] = useState<number[]>(defaultZoneLength);
    const [sigmaS, setSigmaS] = useState<number[]>(defaultSigmaS);
    const [sigmaT, setSigmaT] = useState<number[]>(defaultSigmaT);
    const [source, setSource] = useState<number[]>(defaultSource);
    const [_, setBoundaryValues] = useState<number[]>(defaultBoundaryValues);
    const [supgTuningValue, setSUPGTuningValue] = useState<number>(
        defaultSUPGTuningValue,
    );

    const [visibleZones, setVisibleZones] = useState<boolean[]>([
        false,
        false,
        false,
        false,
        false,
    ]);

    const [gridpoints, setGridpoints] = useState<number[]>([]);
    const [phi, setPhi] = useState<number[]>([]);

    const calculatorRef: React.RefObject<HTMLDivElement | null> = useRef(null);
    const desmosCalc: React.RefObject<Desmos.Calculator | null> = useRef(null);

    useEffect(() => {
        if (!calculatorRef.current) return;

        desmosCalc.current = Desmos.GraphingCalculator(calculatorRef.current, {
            expressions: false,
        });

        return () => {
            if (desmosCalc.current) desmosCalc.current.destroy();
        };
    }, []);

    useEffect(() => {
        if (!desmosCalc.current) return;

        desmosCalc.current.setExpression({
            id: "xlist",
            latex: `X = [${gridpoints.join(",")}]`,
            hidden: true,
        });
        desmosCalc.current.setExpression({
            id: "ylist",
            latex: `Y = [${phi.join(",")}]`,
            hidden: true,
        });

        desmosCalc.current.setExpression({
            id: "points",
            latex: "(X, Y)",
            pointStyle: Desmos.Styles.POINT,
            // showPoints: true,
            lines: true,
        });
    }, [gridpoints, phi]);

    const incrementZones = () => {
        setNZones((n) => n + 1);

        setCells((c) => [...c, 0]);
        setZoneLength((zl) => [...zl, 0]);
        setSigmaS((ss) => [...ss, 0]);
        setSigmaT((st) => [...st, 0]);
        setSource((s) => [...s, 0]);
        setBoundaryValues((bv) => [...bv, 0]);
    };

    const handleSubmit = () => {
        fetch("/api/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                n_angles: 8,
                tol: tol,
                max_iter: maxIter,
                n_zones: nZones,
                n_cells: cells,
                zone_length: zoneLength,
                sigma_s: sigmaS,
                sigma_t: sigmaT,
                source: source,
                boundary_values: [0, 0],
                supg_tuning_value: supgTuningValue,
            }),
        })
            .then((res) => res.json())
            .then((resJSON) => {
                setGridpoints(resJSON.gridpoints);
                setPhi(resJSON.phi);
            })
            .catch((err) => {
                console.error(err);
            });
    };

    return (
        <>
            <div className="flex flex-row">
                <div className="m-5 flex-1/2 text-2xl">
                    <div className="flex flex-row mb-5 justify-between">
                        <div>Radiation Transport Equation</div>
                        <button
                            className="cursor-pointer"
                            onClick={handleSubmit}
                        >
                            Submit
                        </button>
                    </div>
                    <div className="flex flex-row gap-3">
                        <div>Tolerance:</div>
                        <input
                            className="italic"
                            type="number"
                            value={tol}
                            step={0.0001}
                            onChange={(e) => setTol(Number(e.target.value))}
                        />
                    </div>
                    <div className="flex flex-row gap-3 pt-5">
                        <div>Max Iterations:</div>
                        <input
                            className="italic"
                            type="number"
                            value={maxIter}
                            step={10}
                            onChange={(e) =>
                                setMaxIter(parseInt(e.target.value))
                            }
                        />
                    </div>
                    <div className="flex flex-row gap-3 pt-5">
                        <div>Tuning Value:</div>
                        <input
                            className="italic"
                            type="number"
                            value={supgTuningValue}
                            step={0.01}
                            onChange={(e) =>
                                setSUPGTuningValue(Number(e.target.value))
                            }
                        />
                    </div>
                    {[...Array(nZones).keys()].map((zone) => {
                        return (
                            <div key={zone}>
                                <div className="pt-5 flex flex-row justify-between">
                                    <div>Zone {zone + 1}</div>
                                    <button
                                        onClick={() =>
                                            setVisibleZones(
                                                (oldVisibleZones) => {
                                                    const newVisibleZones = [
                                                        ...oldVisibleZones,
                                                    ];
                                                    newVisibleZones[zone] =
                                                        !oldVisibleZones[zone];
                                                    return newVisibleZones;
                                                },
                                            )
                                        }
                                        className="cursor-pointer"
                                    >
                                        Visible
                                    </button>
                                </div>
                                {visibleZones[zone] && (
                                    <>
                                        <div className="flex flex-row gap-3 pt-2 pl-5">
                                            <div>Cells:</div>
                                            <input
                                                className="italic"
                                                type="number"
                                                value={cells[zone]}
                                                step={1}
                                                onChange={(e) =>
                                                    setCells((oldCells) => {
                                                        const newCells = [
                                                            ...oldCells,
                                                        ];
                                                        newCells[zone] =
                                                            parseInt(
                                                                e.target.value,
                                                            );
                                                        return newCells;
                                                    })
                                                }
                                            />
                                        </div>
                                        <div className="flex flex-row gap-3 pt-2 pl-5">
                                            <div>Zone Length:</div>
                                            <input
                                                className="italic"
                                                type="number"
                                                value={zoneLength[zone]}
                                                step={1}
                                                onChange={(e) =>
                                                    setZoneLength(
                                                        (oldZoneLength) => {
                                                            const newZoneLength =
                                                                [
                                                                    ...oldZoneLength,
                                                                ];
                                                            newZoneLength[
                                                                zone
                                                            ] = Number(
                                                                e.target.value,
                                                            );
                                                            return newZoneLength;
                                                        },
                                                    )
                                                }
                                            />
                                        </div>
                                        <div className="flex flex-row gap-3 pt-2 pl-5">
                                            <div>Sigma S:</div>
                                            <input
                                                className="italic"
                                                type="number"
                                                value={sigmaS[zone]}
                                                step={0.01}
                                                onChange={(e) =>
                                                    setSigmaS((oldSigmaS) => {
                                                        const newSigmaS = [
                                                            ...oldSigmaS,
                                                        ];
                                                        newSigmaS[zone] =
                                                            Number(
                                                                e.target.value,
                                                            );
                                                        return newSigmaS;
                                                    })
                                                }
                                            />
                                        </div>
                                        <div className="flex flex-row gap-3 pt-2 pl-5">
                                            <div>Sigma T:</div>
                                            <input
                                                className="italic"
                                                type="number"
                                                value={sigmaT[zone]}
                                                step={0.01}
                                                onChange={(e) =>
                                                    setSigmaS((oldSigmaT) => {
                                                        const newSigmaT = [
                                                            ...oldSigmaT,
                                                        ];
                                                        newSigmaT[zone] =
                                                            Number(
                                                                e.target.value,
                                                            );
                                                        return newSigmaT;
                                                    })
                                                }
                                            />
                                        </div>
                                        <div className="flex flex-row gap-3 pt-2 pl-5">
                                            <div>Source:</div>
                                            <input
                                                className="italic"
                                                type="number"
                                                value={source[zone]}
                                                step={0.01}
                                                onChange={(e) =>
                                                    setSource((oldSource) => {
                                                        const newSource = [
                                                            ...oldSource,
                                                        ];
                                                        newSource[zone] =
                                                            Number(
                                                                e.target.value,
                                                            );
                                                        return newSource;
                                                    })
                                                }
                                            />
                                        </div>
                                    </>
                                )}
                            </div>
                        );
                    })}
                    <button className="cursor-pointer" onClick={incrementZones}>
                        + Zone
                    </button>
                </div>
                <div ref={calculatorRef} className="h-screen w-500" />;
            </div>
        </>
    );
}

export default App;
