import { useState, useEffect, useRef } from "react";
import Slider from "rc-slider";
import "rc-slider/assets/index.css";

type NumberType = "Int" | "Float";
interface Field {
    name: string;
    fieldType: NumberType;
    isZoned: boolean;
    setFieldArr?: React.Dispatch<React.SetStateAction<number[]>>;
    setVal?: React.Dispatch<React.SetStateAction<number>>;
    arr?: number[];
    val?: number;
    min: number;
    max: number;
    step: number;
    isExp: boolean;
}

function App() {
    
    const defaultTol = 0.0001;
    const defaultMaxIter = 1000;
    const defaultSUPGTuningValue = 1;
    const defaultMu = 1;
    const defaultBoundaryValue = 0;

    const defaultNZones = 5;
    const defaultCells = [25, 25, 25, 25, 25];
    const defaultZoneLength = [2, 1, 2, 1, 2];
    const defaultSigmaS = [0, 0, 0, 0.9, 0.9];
    const defaultSigmaT = [50, 5, 0, 1, 1];
    const defaultSource = [25, 0, 0, 0.5, 0];

    // Global Params
    const [tol, setTol] = useState<number>(defaultTol);
    const [maxIter, setMaxIter] = useState<number>(defaultMaxIter);
    const [supgTuningValue, setSUPGTuningValue] = useState<number>(
        defaultSUPGTuningValue,
    );
    const [mu, setMu] = useState<number>(defaultMu)
    const [boundaryValue, setBoundaryValue] = useState<number>(defaultBoundaryValue);

    const [nZones, setNZones] = useState<number>(defaultNZones);
    const [cells, setCells] = useState<number[]>(defaultCells);
    const [zoneLength, setZoneLength] = useState<number[]>(defaultZoneLength);
    const [sigmaS, setSigmaS] = useState<number[]>(defaultSigmaS);
    const [sigmaT, setSigmaT] = useState<number[]>(defaultSigmaT);
    const [source, setSource] = useState<number[]>(defaultSource);

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

    /*
     * Global Parameters
     */
    const globalParamFields: Field[] = [
        {
            name: "Tolerance",
            fieldType: "Float",
            isZoned: false,
            setVal: setTol,
            val: tol,
            min: 0.0001,
            max: 1,
            step: 0.01,
            isExp: true,
        },
        {
            name: "Max Iterations",
            fieldType: "Int",
            isZoned: false,
            setVal: setMaxIter,
            val: maxIter,
            min: 10,
            max: 1000,
            step: 10,
            isExp: false,
        },
        {
            name: "Tuning Value",
            fieldType: "Float",
            isZoned: false,
            setVal: setSUPGTuningValue,
            val: supgTuningValue,
            min: 0,
            max: 10,
            step: 0.01,
            isExp: false,
        },
        {
            name: "μ",
            fieldType: "Float",
            isZoned: false,
            setVal: setMu,
            val: mu,
            min: -1,
            max: 1,
            step: 0.01,
            isExp: false,
        },
        {
            name: "Boundary Value",
            fieldType: "Float",
            isZoned: false,
            setVal: setBoundaryValue,
            val: boundaryValue,
            min: -10,
            max: 10,
            step: 0.1,
            isExp: false,
        }
    ];

    const GlobalParams: React.FC = () => {
        return (
            <div className="border-gray-300 border rounded-lg p-3">
                <div className="font-bold text-lg">Global Parameters</div>
                {globalParamFields.map((field) => {
                    if (field.val === undefined) return <></>
                    const [sliderVal, setSliderVal] = useState<number>(field.val)

                    return (
                        <div key={field.name}>
                            <div className="flex flex-row pt-5 justify-between">
                                <div>{field.name}</div>
                                <input
                                    className="italic text-right w-20 inline-block"
                                    value={sliderVal}
                                    onChange={(e) => {
                                        const parsingFn =
                                            field.fieldType == "Int"
                                                ? parseInt
                                                : Number;
                                        field.setVal?.(
                                            parsingFn(e.target.value),
                                        );
                                    }}
                                />
                            </div>
                            <div className="pl-3 pr-3 pt-1">
                                <Slider
                                    allowCross={false}
                                    min={field.min}
                                    max={field.max}
                                    step={field.step}
                                    value={sliderVal}
                                    onChange={setSliderVal}
                                    onAfterChange={(v:number) => field.setVal?.(v)}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>
        );
    };

    const zoneParams: Field[] = [
        {
            name: "Cells",
            fieldType: "Int",
            isZoned: true,
            setFieldArr: setCells,
            arr: cells,
            min: 1,
            max: 100,
            step: 1,
            isExp: false,
        }
    ]

    return (
        <>
            <div className="flex flex-row">
                <div className="flex-2/5">
                    <div className="font-bold m-5 center text-2xl">
                        Radiation Transport Equation
                    </div>
                    <div className="m-5">
                        <GlobalParams />
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
