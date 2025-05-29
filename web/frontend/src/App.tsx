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
    const defaultNAngles = 8;
    const defaultTol = 0.0001;
    const defaultMaxIter = 1000;
    const defaultSUPGTuningValue = 1;
    const defaultBoundaryValue1 = 0;
    const defaultBoundaryValue2 = 0;

    const defaultNZones = 5;
    const defaultCells = [25, 25, 25, 25, 25];
    const defaultZoneLength = [2, 1, 2, 1, 2];
    const defaultSigmaS = [0, 0, 0, 0.9, 0.9];
    const defaultSigmaT = [50, 5, 0, 1, 1];
    const defaultSource = [25, 0, 0, 0.5, 0];

    // Global Params
    const [nAngles, setNAngles] = useState<number>(defaultNAngles);
    const [tol, setTol] = useState<number>(defaultTol);
    const [maxIter, setMaxIter] = useState<number>(defaultMaxIter);
    const [supgTuningValue, setSUPGTuningValue] = useState<number>(
        defaultSUPGTuningValue,
    );
    const [boundaryValue1, setBoundaryValue1] = useState<number>(
        defaultBoundaryValue1,
    );
    const [boundaryValue2, setBoundaryValue2] = useState<number>(
        defaultBoundaryValue2,
    );

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

    const toggleVisibleZone = (zone: number) => {
        setVisibleZones((oldVisibleZones) => {
            const newVisibleZones = [...oldVisibleZones];
            newVisibleZones[zone] = !oldVisibleZones[zone];
            return newVisibleZones;
        });
    };

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
            lines: true,
            color: Desmos.Colors.BLACK,
        });

        const newTop = Math.max(...phi) + 1;
        const newBottom = Math.min(...phi) - 1;
        const newLeft = Math.min(...gridpoints) - 1;
        const newRight = Math.max(...gridpoints) + 1;

        desmosCalc.current.setMathBounds({
            top: newTop,
            bottom: newBottom,
            left: newLeft,
            right: newRight,
        });

        desmosCalc.current.setDefaultState(desmosCalc.current.getState());
    }, [gridpoints, phi]);

    const incrementZones = () => {
        setNZones((n) => n + 1);

        setCells((c) => [...c, 10]);
        setZoneLength((zl) => [...zl, 2]);
        setSigmaS((ss) => [...ss, 0]);
        setSigmaT((st) => [...st, 50]);
        setSource((s) => [...s, 0]);
    };

    const removeZone = (zone: number) => {
        setNZones((n) => n - 1);

        setCells((c) => c.filter((_, idx) => idx != zone));
        setZoneLength((zl) => zl.filter((_, idx) => idx != zone));
        setSigmaS((ss) => ss.filter((_, idx) => idx != zone));
        setSigmaT((st) => st.filter((_, idx) => idx != zone));
        setSource((s) => s.filter((_, idx) => idx != zone));
    };

    const handleSubmit = () => {
        fetch("/api/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                n_angles: nAngles,
                tol: tol,
                max_iter: maxIter,
                n_zones: nZones,
                n_cells: cells,
                zone_length: zoneLength,
                sigma_s: sigmaS,
                sigma_t: sigmaT,
                source: source,
                boundary_values: [boundaryValue1, boundaryValue2],
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

    useEffect(() => {
        handleSubmit();
    }, [
        nAngles,
        tol,
        maxIter,
        nZones,
        cells,
        zoneLength,
        sigmaS,
        sigmaT,
        source,
        boundaryValue1,
        boundaryValue2,
        supgTuningValue,
    ]);

    /*
     * Global Parameters
     */
    const globalParamFields: Field[] = [
        {
            name: "Angles",
            fieldType: "Int",
            isZoned: false,
            setVal: setNAngles,
            val: nAngles,
            min: 2,
            max: 100,
            step: 2,
            isExp: false,
        },
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
            name: "Boundary Value 1",
            fieldType: "Float",
            isZoned: false,
            setVal: setBoundaryValue1,
            val: boundaryValue1,
            min: 0,
            max: 10,
            step: 0.1,
            isExp: false,
        },
        {
            name: "Boundary Value 2",
            fieldType: "Float",
            isZoned: false,
            setVal: setBoundaryValue2,
            val: boundaryValue2,
            min: 0,
            max: 10,
            step: 0.1,
            isExp: false,
        },
    ];

    const GlobalParams: React.FC = () => {
        return (
            <div className="border-gray-300 border rounded-lg p-3">
                <div className="font-bold text-lg">Global Parameters</div>
                {globalParamFields.map((field) => {
                    if (field.val === undefined) return <></>;
                    const [sliderVal, setSliderVal] = useState<number>(
                        field.val,
                    );

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
                                        setSliderVal(parsingFn(e.target.value));
                                    }}
                                    onBlur={(e) => {
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
                                    min={field.min}
                                    max={field.max}
                                    step={field.step}
                                    value={sliderVal}
                                    styles={{
                                        track: { backgroundColor: "#F49289" },
                                        handle: {
                                            borderColor: "#F49289",
                                            backgroundColor: "white",
                                        },
                                    }}
                                    onChange={(v: number | number[]) =>
                                        setSliderVal(v as number)
                                    }
                                    onChangeComplete={(v: number | number[]) =>
                                        field.setVal?.(v as number)
                                    }
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
        },
        {
            name: "Zone Length",
            fieldType: "Float",
            isZoned: true,
            setFieldArr: setZoneLength,
            arr: zoneLength,
            min: 0.1,
            max: 10,
            step: 0.1,
            isExp: false,
        },
        {
            name: "σˢ",
            fieldType: "Float",
            isZoned: true,
            setFieldArr: setSigmaS,
            arr: sigmaS,
            min: 0,
            max: 100,
            step: 0.1,
            isExp: false,
        },
        {
            name: "σᵗ",
            fieldType: "Float",
            isZoned: true,
            setFieldArr: setSigmaT,
            arr: sigmaT,
            min: 0,
            max: 100,
            step: 0.1,
            isExp: false,
        },
        {
            name: "Source",
            fieldType: "Float",
            isZoned: true,
            setFieldArr: setSource,
            arr: source,
            min: 0,
            max: 100,
            step: 0.1,
            isExp: false,
        },
    ];

    const ZonedParams: React.FC<{ zone: number }> = ({ zone }) => {
        return (
            <div className="mt-5 border-gray-300 border rounded-lg p-3">
                <div className="flex flex-row justify-between">
                    <div
                        className="flex flex-row gap-3 cursor-pointer"
                        onClick={() => toggleVisibleZone(zone)}
                    >
                        {visibleZones[zone] ? (
                            <img src="down-arrow.svg" width={15} />
                        ) : (
                            <img src="right-arrow.svg" width={15} />
                        )}
                        <div>Zone {zone + 1}</div>
                    </div>
                    <button className="cursor-pointer">
                        <img
                            src="cross.svg"
                            width={20}
                            onClick={() => removeZone(zone)}
                        />
                    </button>
                </div>
                {visibleZones[zone] && (
                    <div className="ml-3 mr-3">
                        {zoneParams.map((field) => {
                            if (field.arr === undefined) return <></>;
                            const [sliderVal, setSliderVal] = useState<number>(
                                field.arr[zone],
                            );
                            return (
                                <div key={field.name} className="mt-2">
                                    <div className="flex flex-row justify-between">
                                        <div>{field.name}</div>
                                        <input
                                            className="italic text-right w-20"
                                            value={sliderVal}
                                            onChange={(e) => {
                                                const parsingFn =
                                                    field.fieldType == "Int"
                                                        ? parseInt
                                                        : Number;
                                                setSliderVal(
                                                    parsingFn(e.target.value),
                                                );
                                            }}
                                            onBlur={(e) => {
                                                const parsingFn =
                                                    field.fieldType == "Int"
                                                        ? parseInt
                                                        : Number;
                                                field.setFieldArr?.(
                                                    (oldArr) => {
                                                        const newArr = [
                                                            ...oldArr,
                                                        ];
                                                        newArr[zone] =
                                                            parsingFn(
                                                                e.target.value,
                                                            );
                                                        return newArr;
                                                    },
                                                );
                                            }}
                                        />
                                    </div>
                                    <Slider
                                        min={field.min}
                                        max={field.max}
                                        step={field.step}
                                        value={sliderVal}
                                        styles={{
                                            track: { backgroundColor: "#F49289" },
                                            handle: {
                                                borderColor: "#F49289",
                                                backgroundColor: "white",
                                            },
                                        }}
                                        onChange={(v: number | number[]) =>
                                            setSliderVal(v as number)
                                        }
                                        onChangeComplete={(
                                            v: number | number[],
                                        ) => {
                                            field.setFieldArr?.((oldArr) => {
                                                const newArr = [...oldArr];
                                                newArr[zone] = v as number;
                                                return newArr;
                                            });
                                        }}
                                    />
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        );
    };

    return (
        <>
            <div className="flex flex-row h-screen">
                <div className="flex-2/5 overflow-y-auto">
                    <div className="font-bold m-5 center text-2xl">
                        Radiation Transport Equation
                    </div>
                    <div className="m-5">
                        <GlobalParams />
                    </div>
                    <div className="m-5">
                        <div className="border-gray-300 border rounded-lg p-3">
                            <div className="flex flex-row justify-between">
                                <div className="font-bold text-lg">Zones</div>
                                <button
                                    className="cursor-pointer"
                                    onClick={incrementZones}
                                >
                                    <img src="plus.svg" width={20} />
                                </button>
                            </div>
                            {[...Array(nZones).keys()].map((zone) => {
                                return <ZonedParams key={zone} zone={zone} />;
                            })}
                        </div>
                    </div>
                </div>
                <div ref={calculatorRef} className="h-screen w-500" />;
            </div>
        </>
    );
}

export default App;
