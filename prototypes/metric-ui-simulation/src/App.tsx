import {
  useEffect,
  useMemo,
  useState,
  type CSSProperties,
  type ReactNode,
} from "react";
import "./App.css";
import {
  lifecycleLabels,
  methodContracts,
  mockBuildingZones,
  phaseLabels,
  PHASE_SEQUENCE,
  PREFAB_LIFECYCLE_STAGES,
  type BuildingZone,
  type MethodKey,
  type PhaseKey,
  type PrefabSubMethod,
} from "./mockMetricData";
import {
  calculateLifecycleStageMetrics,
  calculatePhaseStageMetrics,
  type ActiveGeometry,
} from "./calculateMockMetrics";
import { calculateTotalProjectMetrics } from "./calculateTotalProjectMetrics";
import {
  getMethodConstraintKey,
  getMethodFloorConstraint,
  type MethodConstraintKey,
  type MethodFloorConstraint,
} from "./mockMethodConstraints";

const CANVAS_WIDTH = 1920;
const CANVAS_HEIGHT = 1080;

const panelBounds = {
  panel_left_info: { x: 26, y: 22, w: 320, h: 700 },
  panel_top_phase_navigation: { x: 407, y: 22, w: 900, h: 100 },
  panel_main_plan_simulation: { x: 368, y: 162, w: 978, h: 560 },
  panel_right_comparison: { x: 1365, y: 22, w: 530, h: 438 },
  panel_prefab_lifecycle_card: { x: 1365, y: 22, w: 530, h: 438 },
  panel_right_cost_chart: { x: 1365, y: 482, w: 530, h: 240 },
  panel_left_assembly_sequence: { x: 26, y: 739, w: 460, h: 260 },
  panel_method_selection: { x: 506, y: 739, w: 840, h: 260 },
  panel_right_phase_preview: { x: 1365, y: 739, w: 530, h: 260 },
  bar_bottom_status: { x: 0, y: 1030, w: 1920, h: 50 },
} as const;

const neutralContract = {
  label: "Select Method",
  data_model: "phase_based",
  display_mode: "construction_phase_view",
  selected_material: "",
  stages: [],
  baseWarnings: [],
  accent: "#c9b48d",
  accentSoft: "rgba(201, 180, 141, 0.16)",
  glow: "rgba(201, 180, 141, 0.36)",
} as const;

const userFacingAssemblyNotes: Record<MethodKey | "none", string[]> = {
  none: [
    "Choose a method to unlock the scale controls.",
    "Floor limits are prototype assumptions for this simulation.",
    "This stepper can later map to a physical project input.",
  ],
  masonry: [
    "Layered brick assembly drives most wall impact.",
    "Structure and finishing usually dominate local labor.",
    "Good for low- to mid-rise comparisons in this prototype.",
  ],
  "3d_printed": [
    "Foundation and roof still rely on conventional trades.",
    "Wall metrics focus on the printed shell and surface.",
    "Some values stay estimated where research is incomplete.",
  ],
  prefab: [
    "Factory production stays separate from transport and assembly.",
    "Lifecycle data replaces the usual construction phases.",
    "Switch CLT and modular concrete to compare strategies.",
  ],
};

function formatNumber(value: number, digits = 0) {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(value);
}

function formatArea(value: number, digits = 0) {
  return `${formatNumber(value, digits)} m²`;
}

function formatBoundary(value: number, digits = 0) {
  return `${formatNumber(value, digits)} m`;
}

function formatCurrency(value: number, digits = 0) {
  return `€${formatNumber(value, digits)}`;
}

function formatCarbon(value: number, digits = 0) {
  return `${formatNumber(value, digits)} kg CO₂e`;
}

function formatDays(value: number, digits = 1) {
  return `${formatNumber(value, digits)} days`;
}

function formatHours(value: number, digits = 1) {
  return `${formatNumber(value, digits)} hours`;
}

function formatMass(value: number, digits = 0) {
  return `${formatNumber(value, digits)} kg`;
}

function formatCompactNumber(value: number, digits = 1) {
  if (Math.abs(value) >= 1000) {
    return `${formatNumber(value / 1000, digits)}k`;
  }
  return formatNumber(value, digits);
}

function formatCompactCarbon(value: number) {
  return `${formatCompactNumber(value, 1)} kg`;
}

function formatCompactCurrency(value: number) {
  return `€${formatCompactNumber(value, 1)}`;
}

function formatCompactDays(value: number) {
  return `${formatCompactNumber(value, 1)}d`;
}

function formatFloors(value: number) {
  return `${formatNumber(value, 0)} ${value === 1 ? "floor" : "floors"}`;
}

function formatHeight(value: number, digits = 1) {
  return `${formatNumber(value, digits)} m`;
}

function humanizeToken(value: string) {
  return value
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function humanizeMaterialSystem(value: string) {
  const materialMap: Record<string, string> = {
    fired_clay_brick: "Fired clay brick",
    printed_concrete_or_earth_proxy: "Printed concrete / earth proxy",
    timber_clt_prefab: "CLT timber prefab",
    modular_concrete_prefab: "Modular concrete prefab",
  };
  return materialMap[value] ?? humanizeToken(value);
}

function humanizeDataModel(value: string) {
  if (value === "phase_based") {
    return "Phase Mode";
  }
  if (value === "lifecycle_based") {
    return "Lifecycle Mode";
  }
  return humanizeToken(value);
}

function humanizeDisplayMode(value: string) {
  if (value === "construction_phase_view") {
    return "Phase Comparison";
  }
  if (value === "prefab_lifecycle_card") {
    return "Prefab Lifecycle View";
  }
  return humanizeToken(value);
}

function humanizeWarning(value: string) {
  const warningMap: Record<string, string> = {
    lifecycle_only_dataset: "Lifecycle Data Only",
    proxy_source: "Estimated Data",
    time_model_provisional: "Estimated Duration",
    unknown_source: "Source Pending",
    unknown_source_key: "Source Pending",
    missing_normalized_data: "Data Pending",
    using_dev_fallback: "Estimated Data",
  };
  return warningMap[value] ?? humanizeToken(value);
}

function readablePhaseLabel(phaseLabel: string) {
  return phaseLabel.replace(/^\d+\s+/, "");
}

function currentBuildingPartLabel(
  labels: string[],
  isWholeBuilding: boolean,
  selectedCount: number,
) {
  if (isWholeBuilding) {
    return "Whole Building";
  }
  if (selectedCount === 1) {
    return labels[0] ?? "Selected Part";
  }
  return `${selectedCount} building parts`;
}

function describeMethodRange(method: MethodKey) {
  if (method === "prefab") {
    return "CLT 1-8 floors or modular concrete 1-12 floors";
  }
  const constraint = getMethodFloorConstraint(method, "clt");
  return `${constraint.min_floors}-${constraint.max_floors} floors`;
}

function clampFloorValue(value: number, constraint: MethodFloorConstraint) {
  return Math.min(
    constraint.max_floors,
    Math.max(constraint.min_floors, value),
  );
}

function buildFloorLimitNotice(
  rawValue: number,
  constraint: MethodFloorConstraint,
) {
  if (rawValue > constraint.max_floors) {
    return `Maximum for ${constraint.label}: ${constraint.max_floors} floors.`;
  }
  if (rawValue < constraint.min_floors) {
    return `Minimum for ${constraint.label}: ${constraint.min_floors} floor${constraint.min_floors === 1 ? "" : "s"}.`;
  }
  return null;
}

function useCanvasScale() {
  const computeScale = () =>
    Math.max(
      0.35,
      Math.min(
        (window.innerWidth - 40) / CANVAS_WIDTH,
        (window.innerHeight - 40) / CANVAS_HEIGHT,
      ),
    );

  const [scale, setScale] = useState(computeScale);

  useEffect(() => {
    const onResize = () => setScale(computeScale());
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  return scale;
}

function App() {
  const [selectedMethod, setSelectedMethod] = useState<MethodKey | null>(null);
  const [selectedPhase, setSelectedPhase] = useState<PhaseKey>("foundation");
  const [selectedZoneIds, setSelectedZoneIds] = useState<string[]>([]);
  const [hoveredZoneId, setHoveredZoneId] = useState<string | null>(null);
  const [prefabSubMethod, setPrefabSubMethod] =
    useState<PrefabSubMethod>("clt");
  const [floorCount, setFloorCount] = useState(0);
  const [floorsTouched, setFloorsTouched] = useState(false);
  const [floorNotice, setFloorNotice] = useState<string | null>(null);
  const [floorWasClamped, setFloorWasClamped] = useState(false);
  const [debugVisible, setDebugVisible] = useState(false);

  const scale = useCanvasScale();
  const activeContract = selectedMethod
    ? methodContracts[selectedMethod]
    : neutralContract;
  const activeConstraintKey: MethodConstraintKey | null = selectedMethod
    ? getMethodConstraintKey(selectedMethod, prefabSubMethod)
    : null;
  const activeConstraint = selectedMethod
    ? getMethodFloorConstraint(selectedMethod, prefabSubMethod)
    : null;

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key.toLowerCase() === "d") {
        setDebugVisible((current) => !current);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    if (!floorNotice) {
      return undefined;
    }

    const timeoutId = window.setTimeout(() => {
      setFloorNotice(null);
    }, 2400);

    return () => window.clearTimeout(timeoutId);
  }, [floorNotice]);

  const selectedZones = useMemo(
    () => mockBuildingZones.filter((zone) => selectedZoneIds.includes(zone.id)),
    [selectedZoneIds],
  );

  const activeZones =
    selectedZones.length > 0 ? selectedZones : mockBuildingZones;

  const activeGeometry = useMemo<ActiveGeometry>(() => {
    const footprintArea = activeZones.reduce((sum, zone) => sum + zone.area_m2, 0);
    const baseWallSurface = activeZones.reduce(
      (sum, zone) => sum + zone.wall_area_m2,
      0,
    );
    const boundaryLength = activeZones.reduce(
      (sum, zone) => sum + zone.perimeter_m,
      0,
    );
    const appliedFloorCount = activeConstraint ? floorCount : 0;
    const floorHeight = activeConstraint?.floor_height_m ?? 0;
    const totalSelectedArea = footprintArea * appliedFloorCount;
    const totalWallSurface = baseWallSurface * appliedFloorCount;
    const buildingHeight = appliedFloorCount * floorHeight;

    return {
      footprint_area_m2: footprintArea,
      base_wall_surface_m2: baseWallSurface,
      total_selected_area_m2: totalSelectedArea,
      total_wall_surface_m2: totalWallSurface,
      floor_count: appliedFloorCount,
      floor_height_m: floorHeight,
      building_height_m: buildingHeight,
      active_area_m2: totalSelectedArea,
      active_wall_area_m2: totalWallSurface,
      active_perimeter_m: boundaryLength,
      active_zone_ids: activeZones.map((zone) => zone.id),
      active_zone_labels: activeZones.map((zone) => zone.label),
      isWholeBuilding: selectedZones.length === 0,
    };
  }, [activeConstraint, activeZones, floorCount, selectedZones.length]);

  const activeSelectedMaterial = !selectedMethod
    ? "Select a method first"
    : selectedMethod === "prefab"
      ? humanizeMaterialSystem(
          prefabSubMethod === "clt"
            ? "timber_clt_prefab"
            : "modular_concrete_prefab",
        )
      : humanizeMaterialSystem(activeContract.selected_material);

  const activePhaseMetrics = useMemo(() => {
    if (!selectedMethod || selectedMethod === "prefab") {
      return null;
    }
    return calculatePhaseStageMetrics(
      selectedMethod,
      selectedPhase,
      activeGeometry,
    );
  }, [activeGeometry, selectedMethod, selectedPhase]);

  const lifecycleRows = useMemo(() => {
    if (selectedMethod !== "prefab") {
      return [];
    }
    return PREFAB_LIFECYCLE_STAGES.map((stage) =>
      calculateLifecycleStageMetrics(stage, prefabSubMethod, activeGeometry),
    );
  }, [activeGeometry, prefabSubMethod, selectedMethod]);

  const totalProjectMetrics = useMemo(() => {
    if (!selectedMethod) {
      return null;
    }

    return calculateTotalProjectMetrics({
      method: selectedMethod,
      data_model: activeContract.data_model,
      display_mode: activeContract.display_mode,
      sub_method: prefabSubMethod,
      activeGeometry,
    });
  }, [
    activeContract.data_model,
    activeContract.display_mode,
    activeGeometry,
    prefabSubMethod,
    selectedMethod,
  ]);

  const activeWarnings = useMemo(() => {
    if (!selectedMethod) {
      return [];
    }

    const selectionWarnings =
      selectedMethod === "prefab"
        ? lifecycleRows.flatMap((row) => row.warnings)
        : (activePhaseMetrics?.warnings ?? []);

    return [...new Set([...activeContract.baseWarnings, ...selectionWarnings])];
  }, [
    activeContract.baseWarnings,
    activePhaseMetrics?.warnings,
    lifecycleRows,
    selectedMethod,
  ]);

  const totalWarnings = useMemo(
    () => (totalProjectMetrics ? [...new Set(totalProjectMetrics.warnings)] : []),
    [totalProjectMetrics],
  );

  const selectedZoneCount = activeGeometry.isWholeBuilding
    ? 0
    : selectedZoneIds.length;
  const selectionScopeLabel = activeGeometry.isWholeBuilding
    ? "Whole Building"
    : "Selected Building Parts";
  const buildingPartLabel = currentBuildingPartLabel(
    activeGeometry.active_zone_labels,
    activeGeometry.isWholeBuilding,
    selectedZoneCount,
  );
  const focusLabel = !selectedMethod
    ? "No method selected"
    : selectedMethod === "prefab"
      ? "Lifecycle overview"
      : readablePhaseLabel(phaseLabels[selectedPhase]);
  const currentMethodLabel = selectedMethod ? activeContract.label : "Not set";
  const methodRangeLabel = activeConstraint
    ? `Max ${activeConstraint.max_floors} floors`
    : "Select a method first";
  const scopeValue = totalProjectMetrics?.scope_label ?? "Method needed";

  const nextAction = !selectedMethod
    ? "Select a construction method."
    : !floorsTouched
      ? "Set floors for this method, then continue."
      : selectedMethod === "prefab"
        ? selectedZoneCount > 0
          ? "Switch CLT / Modular Concrete or compare another building part."
          : "Switch CLT / Modular Concrete or click a building part."
        : selectedZoneCount > 0
          ? "Change phase or compare another building part."
          : "Choose a phase or click a building part to inspect local impact.";

  const statusHint = !selectedMethod
    ? "Start by selecting a construction method."
    : !floorsTouched
      ? "Now set the number of floors allowed for this method."
      : selectedMethod === "prefab"
        ? "Prefab uses lifecycle mode. Set floors, switch prefab type, or click a building part."
        : selectedZoneCount > 0
          ? "Metrics updated for the selected area. Shift-click to combine building parts."
          : "Choose a phase or click a building part.";

  const currentStep = !selectedMethod ? 1 : !floorsTouched ? 2 : selectedZoneCount > 0 ? 4 : 3;

  const totalMetricRows = totalProjectMetrics
    ? [
        {
          key: "co2",
          label: "Total Carbon",
          value: totalProjectMetrics.total_co2,
          unit: "carbon",
          digits: 0,
        },
        {
          key: "cost",
          label: "Total Cost",
          value: totalProjectMetrics.total_cost,
          unit: "currency",
          digits: 0,
        },
        {
          key: "time",
          label: "Total Time",
          value: totalProjectMetrics.total_time_days,
          unit: "days",
          digits: 1,
        },
        {
          key: "labor",
          label: "Total Labor",
          value: totalProjectMetrics.total_labor_hours,
          unit: "hours",
          digits: 1,
        },
        {
          key: "mass",
          label: "Total Material",
          value: totalProjectMetrics.total_material_mass,
          unit: "mass",
          digits: 0,
        },
      ]
    : [];

  const applyFloorCount = (
    rawValue: number,
    options?: {
      markTouched?: boolean;
      showClampNotice?: boolean;
    },
  ) => {
    if (!activeConstraint || Number.isNaN(rawValue)) {
      return;
    }

    const nextFloorCount = clampFloorValue(rawValue, activeConstraint);
    const didClamp = nextFloorCount !== rawValue;

    setFloorCount(nextFloorCount);
    setFloorWasClamped(didClamp);

    if (options?.markTouched ?? true) {
      setFloorsTouched(true);
    }

    if (didClamp && (options?.showClampNotice ?? true)) {
      setFloorNotice(buildFloorLimitNotice(rawValue, activeConstraint));
    } else if (!didClamp) {
      setFloorNotice(null);
    }
  };

  const handleMethodSelect = (methodKey: MethodKey) => {
    const nextConstraint = getMethodFloorConstraint(methodKey, prefabSubMethod);
    const shouldUseDefault = selectedMethod === null;
    const nextFloorCount = shouldUseDefault
      ? nextConstraint.default_floors
      : clampFloorValue(floorCount, nextConstraint);
    const didClamp = !shouldUseDefault && nextFloorCount !== floorCount;

    setSelectedMethod(methodKey);
    setFloorCount(nextFloorCount);
    setFloorsTouched(false);
    setFloorWasClamped(didClamp);
    setFloorNotice(
      didClamp ? buildFloorLimitNotice(floorCount, nextConstraint) : null,
    );
  };

  const handlePrefabSubMethodChange = (subMethod: PrefabSubMethod) => {
    setPrefabSubMethod(subMethod);

    if (selectedMethod !== "prefab") {
      return;
    }

    const nextConstraint = getMethodFloorConstraint("prefab", subMethod);
    const rawFloorValue =
      floorCount > 0 ? floorCount : nextConstraint.default_floors;
    const nextFloorCount = clampFloorValue(rawFloorValue, nextConstraint);
    const didClamp = nextFloorCount !== rawFloorValue;

    setFloorCount(nextFloorCount);
    setFloorWasClamped(didClamp);
    setFloorNotice(
      didClamp ? buildFloorLimitNotice(rawFloorValue, nextConstraint) : null,
    );
  };

  const handleZoneClick = (zone: BuildingZone, shiftKey: boolean) => {
    if (selectedMethod && !floorsTouched) {
      setFloorsTouched(true);
    }

    setSelectedZoneIds((current) => {
      if (shiftKey) {
        return current.includes(zone.id)
          ? current.filter((zoneId) => zoneId !== zone.id)
          : [...current, zone.id];
      }
      return current.length === 1 && current[0] === zone.id ? [] : [zone.id];
    });
  };

  const renderPanel = (
    id: keyof typeof panelBounds,
    title: string,
    content: ReactNode,
  ) => {
    const bounds = panelBounds[id];
    return (
      <section
        className="panel"
        data-panel-id={id}
        style={{
          left: bounds.x,
          top: bounds.y,
          width: bounds.w,
          height: bounds.h,
        }}
      >
        <div className="panelHeader">
          {debugVisible ? (
            <span className="panelEyebrow">{id.split("_").join(" ")}</span>
          ) : null}
          <h2>{title}</h2>
        </div>
        <div className="panelBody">{content}</div>
      </section>
    );
  };

  return (
    <div className="viewport">
      <div
        className="canvasScaler"
        style={{
          width: CANVAS_WIDTH * scale,
          height: CANVAS_HEIGHT * scale,
        }}
      >
        <div
          id="canvas_main"
          className="canvasMain"
          style={
            {
              transform: `scale(${scale})`,
              "--accent": activeContract.accent,
              "--accent-soft": activeContract.accentSoft,
              "--accent-glow": activeContract.glow,
            } as CSSProperties
          }
        >
          {renderPanel(
            "panel_left_info",
            "Your Selection",
            <div
              className="infoStack fadePane"
              key={`info-${selectedMethod ?? "none"}-${prefabSubMethod}-${selectedPhase}-${selectedZoneIds.join("-")}-${floorCount}`}
            >
              <div className="heroCard">
                <div className="heroCardTop">
                  <span className="heroEyebrow">Method</span>
                  <div className="badgeRail">
                    {selectedMethod ? (
                      <span className="softBadge">
                        {humanizeDataModel(activeContract.data_model)}
                      </span>
                    ) : (
                      <span className="softBadge neutral">Step 1</span>
                    )}
                  </div>
                </div>
                <div className="heroTitle">
                  {selectedMethod ? activeContract.label : "Choose A Method"}
                </div>
                <div className="heroSubtitle">
                  {!selectedMethod
                    ? "Select a construction method to unlock the rest of the interface."
                    : selectedMethod === "prefab"
                      ? "Prefab stays in lifecycle mode instead of construction phases."
                      : "Set floors, then inspect a phase and building part."}
                </div>
              </div>

              <div className="infoCard">
                <div className="infoCardTitle">Selection Details</div>
                <div className="keyValueList">
                  <div>
                    <span>Building Part</span>
                    <strong>{buildingPartLabel}</strong>
                  </div>
                  <div>
                    <span>Footprint Area</span>
                    <strong>{formatArea(activeGeometry.footprint_area_m2)}</strong>
                  </div>
                  <div>
                    <span>Boundary Length</span>
                    <strong>{formatBoundary(activeGeometry.active_perimeter_m)}</strong>
                  </div>
                  <div>
                    <span>Material System</span>
                    <strong>{activeSelectedMaterial}</strong>
                  </div>
                </div>
                <div className="chipWrap compact">
                  <span className="softBadge">{selectionScopeLabel}</span>
                  <span className="softBadge neutral">
                    {selectedZoneCount > 0
                      ? `${selectedZoneCount} selected`
                      : "Whole building"}
                  </span>
                </div>
              </div>

              <div className="infoCard">
                <div className="infoCardTitle">Building Scale</div>
                {!selectedMethod || !activeConstraint ? (
                  <div className="emptyStateCard">
                    <strong>Select a method first</strong>
                    <p className="bodyCopy">
                      Floors become method-dependent after you choose a
                      construction system.
                    </p>
                  </div>
                ) : (
                  <div className="floorControlStack">
                    <div className="floorHeader">
                      <div>
                        <span className="microLabel">Floors</span>
                        <strong>{formatNumber(floorCount)}</strong>
                      </div>
                      <div className="floorMeta">
                        <span className="microLabel">Floor Height</span>
                        <strong>{formatHeight(activeConstraint.floor_height_m)}</strong>
                      </div>
                    </div>

                    <div className="floorStepper">
                      <button
                        type="button"
                        className="stepperButton"
                        onClick={() => applyFloorCount(floorCount - 1)}
                        disabled={floorCount <= activeConstraint.min_floors}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        className="stepperInput"
                        min={activeConstraint.min_floors}
                        max={activeConstraint.max_floors}
                        value={floorCount}
                        onChange={(event) =>
                          applyFloorCount(Number(event.target.value))
                        }
                        onBlur={(event) =>
                          applyFloorCount(Number(event.target.value))
                        }
                      />
                      <button
                        type="button"
                        className="stepperButton"
                        onClick={() => applyFloorCount(floorCount + 1)}
                        disabled={floorCount >= activeConstraint.max_floors}
                      >
                        +
                      </button>
                    </div>

                    <div className="rangeNote">
                      Max for this method: {activeConstraint.max_floors} floors
                    </div>
                    <div className="rangeNote subdued">
                      {activeConstraint.user_note}
                    </div>
                    {floorNotice ? (
                      <div className="floorNotice">{floorNotice}</div>
                    ) : null}

                    <div className="keyValueList compactList">
                      <div>
                        <span>Total Selected Area</span>
                        <strong>
                          {formatArea(activeGeometry.total_selected_area_m2)}
                        </strong>
                      </div>
                      <div>
                        <span>Wall Surface</span>
                        <strong>
                          {formatArea(activeGeometry.total_wall_surface_m2)}
                        </strong>
                      </div>
                      <div>
                        <span>Building Height</span>
                        <strong>
                          {formatHeight(activeGeometry.building_height_m)}
                        </strong>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="infoCard">
                <div className="infoCardTitle">Helper</div>
                <p className="bodyCopy">
                  Click a building part. Shift-click to compare.
                </p>
              </div>
            </div>,
          )}

          {renderPanel(
            "panel_top_phase_navigation",
            "Choose Phase",
            <div className="phaseNavWrap">
              <div
                className={`phaseNav ${
                  !selectedMethod || selectedMethod === "prefab"
                    ? "phaseNavDisabled"
                    : ""
                }`}
              >
                {PHASE_SEQUENCE.map((phase) => (
                  <button
                    key={phase}
                    type="button"
                    className={`phaseChip ${selectedPhase === phase ? "active" : ""}`}
                    onClick={() => {
                      if (!selectedMethod || selectedMethod === "prefab") {
                        return;
                      }
                      if (!floorsTouched) {
                        setFloorsTouched(true);
                      }
                      setSelectedPhase(phase);
                    }}
                    disabled={!selectedMethod || selectedMethod === "prefab"}
                  >
                    {phaseLabels[phase]}
                  </button>
                ))}
              </div>
              <div className="phaseNavNote">
                {!selectedMethod
                  ? "Select a method, then set floors to unlock phases."
                  : selectedMethod === "prefab"
                    ? "Lifecycle mode active. Construction phases stay disabled."
                    : "Choose a phase to inspect local impact."}
              </div>
            </div>,
          )}

          {renderPanel(
            "panel_main_plan_simulation",
            "Choose Building Part",
            <div className="planShell">
              <div className="planHeaderMeta">
                <span className="softBadge">{selectionScopeLabel}</span>
                <span className="softBadge neutral">
                  {activeGeometry.isWholeBuilding
                    ? "No building part selected"
                    : `${selectedZoneCount} parts selected`}
                </span>
                {selectedMethod && activeConstraint ? (
                  <span className="softBadge neutral">
                    {formatFloors(floorCount)} active
                  </span>
                ) : null}
              </div>
              <svg
                className="planSvg"
                viewBox="0 0 978 560"
                role="presentation"
                onClick={() => {
                  if (selectedMethod && !floorsTouched) {
                    setFloorsTouched(true);
                  }
                  setSelectedZoneIds([]);
                }}
              >
                <rect
                  x="24"
                  y="22"
                  width="930"
                  height="512"
                  rx="28"
                  className="planFrame"
                />
                {mockBuildingZones.map((zone) => {
                  const isSelected =
                    selectedZoneIds.length > 0 && selectedZoneIds.includes(zone.id);
                  const isHovered = hoveredZoneId === zone.id;
                  return (
                    <g key={zone.id}>
                      <rect
                        x={zone.shape.x}
                        y={zone.shape.y}
                        width={zone.shape.w}
                        height={zone.shape.h}
                        rx={zone.shape.rx ?? 0}
                        className={`planZone ${isSelected ? "selected" : ""} ${
                          isHovered ? "hovered" : ""
                        } ${zone.id === "zone_facade_band" ? "facadeBand" : ""}`}
                        onClick={(event) => {
                          event.stopPropagation();
                          handleZoneClick(zone, event.shiftKey);
                        }}
                        onMouseEnter={() => setHoveredZoneId(zone.id)}
                        onMouseLeave={() => setHoveredZoneId(null)}
                      />
                      <text
                        x={zone.shape.x + zone.shape.w / 2}
                        y={zone.shape.y + zone.shape.h / 2}
                        className="planZoneLabel"
                      >
                        {zone.label}
                      </text>
                    </g>
                  );
                })}
              </svg>
              <div className="planLegend">
                <span>Click to select a building part.</span>
                <span>Shift + click to compare multiple building parts.</span>
                <span>Click empty space to return to whole-building scope.</span>
              </div>
            </div>,
          )}

          {selectedMethod === "prefab"
            ? renderPanel(
                "panel_prefab_lifecycle_card",
                "Prefab Lifecycle Impact",
                <div
                  className="lifecycleCard fadePane"
                  key={`prefab-${prefabSubMethod}-${selectedZoneIds.join("-")}-${floorCount}`}
                >
                  <div className="badgeRow">
                    <div className="chipWrap compact">
                      <span className="successBadge">Lifecycle Data Only</span>
                      <span className="softBadge neutral">
                        {formatFloors(floorCount)}
                      </span>
                    </div>
                    <div className="subMethodToggle">
                      {(["clt", "modular_concrete"] as PrefabSubMethod[]).map(
                        (subMethod) => (
                          <button
                            key={subMethod}
                            type="button"
                            className={`subMethodButton ${
                              prefabSubMethod === subMethod ? "active" : ""
                            }`}
                            onClick={() =>
                              handlePrefabSubMethodChange(subMethod)
                            }
                          >
                            {subMethod === "clt"
                              ? "CLT / Timber Prefab"
                              : "Modular Concrete Prefab"}
                          </button>
                        ),
                      )}
                    </div>
                  </div>
                  <p className="bodyCopy calmCopy">
                    Lifecycle mode active. Prefab data follows lifecycle stages.
                  </p>
                  <div className="chipWrap compact">
                    <span className="softBadge">{selectionScopeLabel}</span>
                    <span className="softBadge neutral">
                      {selectedZoneCount > 0
                        ? `${selectedZoneCount} parts selected`
                        : "Whole building active"}
                    </span>
                  </div>
                  <div className="lifecycleRows">
                    {lifecycleRows.map((row) => (
                      <div key={row.stage} className="lifecycleRow">
                        <div className="lifecycleRowCopy">
                          <strong>{row.stage}</strong>
                          <span>{lifecycleLabels[row.stage]}</span>
                        </div>
                        <div className="lifecycleRowMetrics">
                          <span>{formatCompactCarbon(row.co2_total)}</span>
                          <span>{formatCompactCurrency(row.cost_total)}</span>
                          <span>{formatCompactDays(row.time_days)}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="basisCard">
                    <div className="basisTitle">Selection Basis</div>
                    <div className="basisInline">
                      <span>{formatArea(activeGeometry.total_selected_area_m2)}</span>
                      <span>{formatArea(activeGeometry.total_wall_surface_m2)}</span>
                      <span>{formatFloors(floorCount)}</span>
                    </div>
                  </div>
                </div>,
              )
            : renderPanel(
                "panel_right_comparison",
                "Selected Part Impact",
                !selectedMethod ? (
                  <div className="comparisonPanel fadePane">
                    <div className="emptyStateCard">
                      <strong>Select a method first</strong>
                      <p className="bodyCopy">
                        Active impact appears here after you choose a
                        construction method and set floors.
                      </p>
                    </div>
                  </div>
                ) : (
                  <div
                    className="comparisonPanel fadePane"
                    key={`active-${selectedMethod}-${selectedPhase}-${selectedZoneIds.join("-")}-${floorCount}`}
                  >
                    <div className="comparisonHeader">
                      <div>
                        <div className="heroEyebrow">Method</div>
                        <div className="comparisonTitle">{activeContract.label}</div>
                        <div className="comparisonMeta">
                          {readablePhaseLabel(phaseLabels[selectedPhase])} ·{" "}
                          {buildingPartLabel}
                        </div>
                      </div>
                      <div className="chipWrap compact">
                        <span className="softBadge">
                          {humanizeDataModel(activeContract.data_model)}
                        </span>
                        <span className="softBadge neutral">
                          {formatFloors(floorCount)}
                        </span>
                      </div>
                    </div>

                    <div className="heroMetricGrid">
                      <div className="heroMetricCard primary">
                        <span>Carbon</span>
                        <strong>
                          {formatCarbon(activePhaseMetrics?.co2_total ?? 0)}
                        </strong>
                      </div>
                      <div className="heroMetricCard">
                        <span>Cost</span>
                        <strong>
                          {formatCurrency(activePhaseMetrics?.cost_total ?? 0)}
                        </strong>
                      </div>
                    </div>

                    <div className="comparisonSecondaryGrid">
                      <div className="miniStat">
                        <span>Time</span>
                        <strong>
                          {formatDays(activePhaseMetrics?.time_days ?? 0, 1)}
                        </strong>
                      </div>
                      <div className="miniStat">
                        <span>Labor</span>
                        <strong>
                          {formatHours(activePhaseMetrics?.labor_hours ?? 0, 1)}
                        </strong>
                      </div>
                      <div className="miniStat">
                        <span>Material</span>
                        <strong>
                          {formatMass(activePhaseMetrics?.material_mass ?? 0)}
                        </strong>
                      </div>
                    </div>

                    <div className="basisCard">
                      <div className="basisTitle">Selection Basis</div>
                      <div className="basisInline">
                        <span>{formatArea(activeGeometry.total_selected_area_m2)}</span>
                        <span>{formatArea(activeGeometry.total_wall_surface_m2)}</span>
                        <span>{formatFloors(floorCount)}</span>
                      </div>
                    </div>
                  </div>
                ),
              )}

          {renderPanel(
            "panel_right_cost_chart",
            "Total Project Impact",
            !totalProjectMetrics ? (
              <div className="totalMetricsPanel fadePane">
                <div className="emptyStateCard">
                  <strong>Select a method first</strong>
                  <p className="bodyCopy">
                    Total project metrics appear here after method selection.
                  </p>
                </div>
              </div>
            ) : (
              <div
                className="totalMetricsPanel fadePane"
                key={`totals-${selectedMethod}-${prefabSubMethod}-${selectedZoneIds.join("-")}-${floorCount}`}
              >
                <div className="totalsHeader">
                  <div>
                    <div className="totalsEyebrow">Scope</div>
                    <div className="totalsScope">{scopeValue}</div>
                  </div>
                  <div className="chipWrap compact">
                    {totalWarnings.slice(0, 2).map((warning) => (
                      <span key={warning} className="warningBadge compact">
                        {humanizeWarning(warning)}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="totalsHero">
                  <span>Total Cost</span>
                  <strong>{formatCurrency(totalProjectMetrics.total_cost)}</strong>
                  <div className="totalsHeroSub">
                    Total Carbon {formatCarbon(totalProjectMetrics.total_co2)}
                  </div>
                </div>

                <div className="totalsGrid">
                  {totalMetricRows.map((metric) => (
                    <div key={metric.key} className="totalMetricCell">
                      <span>{metric.label}</span>
                      <strong>
                        {metric.unit === "currency"
                          ? formatCurrency(metric.value, metric.digits)
                          : metric.unit === "carbon"
                            ? formatCarbon(metric.value, metric.digits)
                            : metric.unit === "days"
                              ? formatDays(metric.value, metric.digits)
                              : metric.unit === "hours"
                                ? formatHours(metric.value, metric.digits)
                                : formatMass(metric.value, metric.digits)}
                      </strong>
                    </div>
                  ))}
                </div>
              </div>
            ),
          )}

          {renderPanel(
            "panel_left_assembly_sequence",
            "Method Notes",
            <div className="sequencePanel">
              <div className="sequenceNotes">
                {userFacingAssemblyNotes[selectedMethod ?? "none"]
                  .slice(0, 2)
                  .map((note) => (
                  <div key={note} className="sequenceItem">
                    <span className="sequenceDot" />
                    <span>{note}</span>
                  </div>
                ))}
              </div>
              <div className="sequenceDivider" />
              <div className="sequenceFocus">
                <div className="infoCardTitle">
                  {selectedMethod === "prefab" ? "Lifecycle Path" : "Phase Path"}
                </div>
                <div className="sequencePillRow">
                  {!selectedMethod
                    ? ["Choose method", "Set floors", "Inspect part"].map((step) => (
                        <span key={step} className="sequencePill">
                          {step}
                        </span>
                      ))
                    : selectedMethod === "prefab"
                      ? PREFAB_LIFECYCLE_STAGES.map((stage) => (
                          <span key={stage} className="sequencePill">
                            {stage}
                          </span>
                        ))
                      : PHASE_SEQUENCE.map((phase) => (
                          <span
                            key={phase}
                            className={`sequencePill ${
                              selectedPhase === phase ? "active" : ""
                            }`}
                          >
                            {phaseLabels[phase]}
                          </span>
                        ))}
                </div>
                <p className="bodyCopy sequenceBody">
                  {!selectedMethod
                    ? "Choose a method to reveal the active path."
                    : selectedMethod === "prefab"
                      ? "Use the prefab toggle to compare lifecycle strategies."
                      : `Current focus: ${readablePhaseLabel(phaseLabels[selectedPhase])}.`}
                </p>
              </div>
            </div>,
          )}

          {renderPanel(
            "panel_method_selection",
            "Choose Method",
            <div className="methodGrid">
              {(Object.keys(methodContracts) as MethodKey[]).map((methodKey) => {
                const method = methodContracts[methodKey];
                const isActive = selectedMethod === methodKey;
                return (
                  <button
                    key={methodKey}
                    type="button"
                    className={`methodCard ${isActive ? "active" : ""}`}
                    onClick={() => handleMethodSelect(methodKey)}
                  >
                    <div className="methodCardTop">
                      <span className="methodTag">
                        {humanizeDataModel(method.data_model)}
                      </span>
                      <span className="methodMode">
                        {humanizeDisplayMode(method.display_mode)}
                      </span>
                    </div>
                    <strong>{method.label}</strong>
                    <p>{humanizeMaterialSystem(method.selected_material)}</p>
                    <div className="methodRangeCopy">
                      Range: {describeMethodRange(methodKey)}
                    </div>
                    <div className="chipWrap">
                      {method.baseWarnings.length > 0 ? (
                        method.baseWarnings.map((warning) => (
                          <span key={warning} className="warningBadge compact">
                            {humanizeWarning(warning)}
                          </span>
                        ))
                      ) : (
                        <span className="softBadge neutral">
                          Ready to compare
                        </span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>,
          )}

          {renderPanel(
            "panel_right_phase_preview",
            "Current State",
            <div
              className="previewPanel fadePane"
              key={`preview-${selectedMethod ?? "none"}-${prefabSubMethod}-${selectedPhase}-${selectedZoneIds.join("-")}-${floorCount}`}
            >
              <div className="previewHeadline">
                <div>
                  <strong>{selectedMethod ? activeContract.label : "Awaiting Method"}</strong>
                  <span>{focusLabel}</span>
                </div>
                {selectedMethod ? (
                  <div className="chipWrap compact">
                    <span className="softBadge">
                      {humanizeDataModel(activeContract.data_model)}
                    </span>
                    <span className="softBadge neutral">
                      {selectedMethod === "prefab"
                        ? "Lifecycle Mode"
                        : "Phase Mode"}
                    </span>
                  </div>
                ) : null}
              </div>

              <div className="previewStats">
                <div className="previewStat">
                  <span>Building Parts</span>
                  <strong>
                    {activeGeometry.isWholeBuilding
                      ? "Whole Building"
                      : `${selectedZoneCount} selected`}
                  </strong>
                </div>
                <div className="previewStat">
                  <span>Current Focus</span>
                  <strong>{focusLabel}</strong>
                </div>
                <div className="previewStat">
                  <span>Floors</span>
                  <strong>
                    {selectedMethod && activeConstraint
                      ? formatFloors(floorCount)
                      : "Not set"}
                  </strong>
                </div>
                <div className="previewStat">
                  <span>Method Range</span>
                  <strong>{methodRangeLabel}</strong>
                </div>
              </div>

              <div className="previewMetaList">
                <div className="previewMetaItem">
                  <span>Current Method</span>
                  <strong>{currentMethodLabel}</strong>
                </div>
                <div className="previewMetaItem">
                  <span>Mode</span>
                  <strong>
                    {selectedMethod
                      ? humanizeDataModel(activeContract.data_model)
                      : "Choose method first"}
                  </strong>
                </div>
                {selectedMethod === "prefab" ? (
                  <div className="previewMetaItem">
                    <span>Prefab Type</span>
                    <strong>
                      {prefabSubMethod === "clt"
                        ? "CLT / Timber Prefab"
                        : "Modular Concrete Prefab"}
                    </strong>
                  </div>
                ) : null}
              </div>

              <div className="infoCard previewCard">
                <div className="infoCardTitle">Next Suggested Action</div>
                <p className="bodyCopy">{nextAction}</p>
              </div>

              <div className="chipWrap">
                {activeWarnings.length > 0 ? (
                  activeWarnings.map((warning) => (
                    <span key={warning} className="warningBadge compact">
                      {humanizeWarning(warning)}
                    </span>
                  ))
                ) : (
                  <span className="softBadge neutral">
                    {selectedMethod ? "Ready for review" : "Waiting for method"}
                  </span>
                )}
              </div>
            </div>,
          )}

          <div
            className="statusBar"
            style={{
              left: panelBounds.bar_bottom_status.x,
              top: panelBounds.bar_bottom_status.y,
              width: panelBounds.bar_bottom_status.w,
              height: panelBounds.bar_bottom_status.h,
            }}
          >
            <div className="statusSteps">
              <span
                className={`statusStep ${currentStep > 1 ? "complete" : "current"}`}
              >
                1 Choose Method
              </span>
              <span
                className={`statusStep ${
                  currentStep === 2 ? "current" : ""
                } ${currentStep > 2 ? "complete" : ""}`}
              >
                2 Set Floors
              </span>
              <span
                className={`statusStep ${
                  currentStep === 3 ? "current" : ""
                } ${currentStep > 3 ? "complete" : ""}`}
              >
                3 {selectedMethod === "prefab" ? "Lifecycle Mode" : "Choose Phase"}
              </span>
              <span className={`statusStep ${currentStep === 4 ? "current" : ""}`}>
                4 Click Building Part
              </span>
            </div>
            <div className="statusHint">{statusHint}</div>
            <div className="statusMeta">Press D for debug</div>
          </div>

          {debugVisible && (
            <>
              {Object.entries(panelBounds).map(([panelId, bounds]) => (
                <div
                  key={panelId}
                  className="debugPanelOutline"
                  style={{
                    left: bounds.x,
                    top: bounds.y,
                    width: bounds.w,
                    height: bounds.h,
                  }}
                >
                  <span>
                    {panelId} [{bounds.x}, {bounds.y}, {bounds.w}, {bounds.h}]
                  </span>
                </div>
              ))}
              <div className="debugOverlay">
                <div>selected method: {selectedMethod ?? "none"}</div>
                <div>active method constraint key: {activeConstraintKey ?? "none"}</div>
                <div>data_model: {selectedMethod ? activeContract.data_model : "none"}</div>
                <div>
                  display_mode: {selectedMethod ? activeContract.display_mode : "none"}
                </div>
                <div>selected phase: {selectedPhase}</div>
                <div>selected prefab sub_method: {prefabSubMethod}</div>
                <div>
                  selected_material:{" "}
                  {selectedMethod ? activeContract.selected_material : "none"}
                </div>
                <div>
                  selected zone IDs: {selectedZoneIds.join(", ") || "whole building"}
                </div>
                <div>footprint_area_m2: {formatNumber(activeGeometry.footprint_area_m2, 1)}</div>
                <div>
                  total_selected_area_m2:{" "}
                  {formatNumber(activeGeometry.total_selected_area_m2, 1)}
                </div>
                <div>
                  base_wall_surface_m2:{" "}
                  {formatNumber(activeGeometry.base_wall_surface_m2, 1)}
                </div>
                <div>
                  total_wall_surface_m2:{" "}
                  {formatNumber(activeGeometry.total_wall_surface_m2, 1)}
                </div>
                <div>active_perimeter_m: {formatNumber(activeGeometry.active_perimeter_m, 1)}</div>
                <div>floor_count: {floorCount}</div>
                <div>min_floors: {activeConstraint?.min_floors ?? "n/a"}</div>
                <div>max_floors: {activeConstraint?.max_floors ?? "n/a"}</div>
                <div>default_floors: {activeConstraint?.default_floors ?? "n/a"}</div>
                <div>floor_height_m: {activeConstraint?.floor_height_m ?? "n/a"}</div>
                <div>building_height_m: {formatNumber(activeGeometry.building_height_m, 1)}</div>
                <div>floor_count_clamped: {floorWasClamped ? "true" : "false"}</div>
                <div>source_key: mock_metric_data</div>
                <div>
                  unit_basis:{" "}
                  {totalProjectMetrics?.calculation_basis.unit_basis_used.join(" | ") ??
                    "method needed"}
                </div>
                <div>
                  active total cost:{" "}
                  {formatNumber(totalProjectMetrics?.total_cost ?? 0, 1)}
                </div>
                <div>
                  active total co2:{" "}
                  {formatNumber(totalProjectMetrics?.total_co2 ?? 0, 1)}
                </div>
                <div>warning codes: {totalWarnings.join(", ") || "none"}</div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
